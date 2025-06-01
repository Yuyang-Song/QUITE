import os
import re
import sys
from typing import List, Dict, Set, Optional, Union
from collections import deque, defaultdict
from time import perf_counter  
from dataclasses import dataclass
from pydantic import BaseModel
from dataclasses import replace
from gpt_request import GPT
sys.path.append('../')
sys.path.append('./utils')
sys.path.append('./')

# os.environ['HTTP_PROXY'] = 'socks5h://127.0.0.1:1080'
# os.environ['HTTPS_PROXY'] = 'socks5h://127.0.0.1:1080'
    
class MessageContent(BaseModel):
    """统一的消息内容结构"""
    timestamp: float = perf_counter()  # 替换time.time()
    text: str
    # metadata: Dict = {}

@dataclass
class Message:
    sent_from: str
    role: str
    content: MessageContent  
    send_to: Optional[str] = None
    timestamp: float = perf_counter()  # 替换time.time()

    def __post_init__(self):
        # 统一转换为MessageContent
        if isinstance(self.content, dict):
            self.content = MessageContent(**self.content)
        elif not isinstance(self.content, MessageContent):
            raise ValueError("Invalid content type, must be MessageContent or dict")

class MemoryWindow:
    """滑动窗口内存容器"""
    def __init__(self, max_size: int = 5):
        self.max_size = max_size
        self.window = deque(maxlen=max_size)
        # 按发送者维护的索引 {sender: deque}
        self.sender_index = defaultdict(lambda: deque(maxlen=max_size))

    def add(self, message: Message):
        self.window.append(message)
        self.sender_index[message.sent_from].append(message)

    def get_recent(self, k: int) -> List[Message]:
        return list(self.window)[-k:] if k > 0 else list(self.window)

    def get_by_sender(self, sender: str, k: int) -> List[Message]:
        return list(self.sender_index.get(sender, deque()))[-k:]

class MessageQueue:
    """增强型消息队列系统"""
    def __init__(self, window_size: int = 10):
        # 完整消息存储
        self.full_history = []
        # 滑动窗口内存
        self.memory_window = MemoryWindow(window_size)
        # 观察关系 {被观察者: 观察者集合}
        self.observation_graph = defaultdict(set)
        # 反向索引 {观察者: 被观察者集合}
        self.reverse_observation_index = defaultdict(set)
        self.registered_agents = set()  # 新增注册表
        self.seen_messages = set()  # 用于去重
    
    def register_agent(self, name: str):
        self.registered_agents.add(name)
    
    def _add_copy(self, message: Message):
        """安全添加副本（更新哈希计算方式）"""
        copy_hash = hash((
            message.sent_from, 
            message.content.text,
            message.send_to  # 包含接收者信息
        ))
        if copy_hash not in self.seen_messages:
            self.memory_window.add(message)
            self.seen_messages.add(copy_hash)

    def add_message(self, message: Message):
        # 处理发送给自己的消息
        if message.send_to == message.sent_from:
            self._add_copy(message)
            return

        # 处理广播消息
        if message.send_to == "all":
            self.full_history.append(message)  # 存储原始记录
            # 创建一条广播消息副本，send_to设为"all"
            broadcast_msg = replace(message, send_to="all")
            self._add_copy(broadcast_msg)
            return

        # 普通消息处理
        unique_hash = hash((message.sent_from, message.content.text, message.send_to))
        if unique_hash in self.seen_messages:
            return
        
        self.full_history.append(message)
        self.memory_window.add(message)
        self.seen_messages.add(unique_hash)

        # 观察者逻辑
        for observer in self.observation_graph.get(message.sent_from, set()):
            if all([
                observer != message.sent_from,
                message.send_to != observer,
                message.role != "system",
                not message.send_to.startswith("_"),
                message.send_to != message.sent_from
            ]):
                copy_msg = replace(message, send_to=observer)
                self._add_copy(copy_msg)
            
    def watch_agent(self, target: str, observer: str):
        """建立观察关系"""
        self.observation_graph[target].add(observer)
        self.reverse_observation_index[observer].add(target)

    def get_memories(self, 
                    observer: Optional[str] = None,
                    k: int = 5,
                    strategy: str = 'recent') -> List[Message]:
        """
        修改后的记忆检索方法
        """
        if not observer:
            return self.memory_window.get_recent(k)

        targets = self.reverse_observation_index.get(observer, set())
        observed_messages = []

        # 获取观察目标的消息（原有逻辑）
        if strategy == 'per_sender':
            observed_messages = self._get_per_sender_memories(targets, observer, k)
        elif strategy == 'recent':
            observed_messages = self._get_recent_memories(targets, observer, k)
        else:
            observed_messages = []

        # 新增：获取直接发送给观察者的消息（包括自己发给自己的）
        direct_messages = [
            msg for msg in self.memory_window.get_recent(2*k)
            if msg.send_to == observer
        ]

        # 获取所有广播消息（send_to为all）
        broadcast_messages = [
            msg for msg in self.memory_window.get_recent(2*k)
            if msg.send_to == "all"
        ]
        
        combined = sorted(
        [(i, msg) for i, msg in enumerate(observed_messages + broadcast_messages + direct_messages)],
        key=lambda x: (x[1].timestamp, -x[0]),  # 时间戳优先，插入顺序其次
        reverse=True
        )
        unique_messages = [msg for _, msg in combined][:k]
        
        return unique_messages[:k]

    def _get_per_sender_memories(self, targets: Set[str], observer: str, k: int) -> List[Message]:
        """从每个目标获取最近的k条消息，且接收者是observer或all"""
        results = []
        for target in targets:
            messages = self.memory_window.get_by_sender(target, k*2)
            filtered = [
                msg for msg in messages
                if msg.send_to in {observer, "all"}  # 包含观察者或广播消息
            ]
            results.extend(filtered[:k])
        return sorted(results, key=lambda x: x.timestamp, reverse=True)[:k]

    def _get_recent_memories(self, targets: Set[str], observer: str, k: int) -> List[Message]:
        """获取所有相关目标的最新k条消息，且接收者是observer或all"""
        candidates = [
            msg for msg in self.memory_window.get_recent(k*2)
            if msg.sent_from in targets and msg.send_to in {observer, "all"}
        ]
        return candidates[-k:]
    


class Agent:
    """增强型Agent基类"""
    def __init__(self, name: str, message_queue: MessageQueue, gpt: GPT):
        self.name = name
        self.llm = gpt  
        self.mq = message_queue
        self.mq.register_agent(name)  # 注册Agent
        self.observation_strategy = 'per_sender'  # 默认观察策略

    def watch(self, targets: List[str]):
        """建立观察关系"""
        for target in targets:
            self.mq.watch_agent(target, self.name)

    def retrieve_memories(self, k: int = 5, strategy: Optional[str] = None) -> List[Message]:
        """记忆检索入口"""
        return self.mq.get_memories(
            observer=self.name,
            k=k,
            strategy=strategy if strategy is not None else self.observation_strategy
        )

    # def retrieve_memories(self, k: int = 5) -> List[Message]:
    #     """记忆检索入口""" 
    #     return self.mq.get_memories( observer=self.name, k=k, strategy=self.observation_strategy )
    
    def format_memories(self, messages: List[Message]) -> str:
        formatted = []
        for msg in messages:
            if msg.send_to is None:
                continue
            entry = f"[{msg.timestamp}] {msg.sent_from} -> {msg.send_to}:\n"
            entry += f"Text: {msg.content.text}\n"
            formatted.append(entry)
        return "\n\n".join(formatted)

    def _extract_sql(self, text):
        sql_code = re.search(r'```sql(.*?)```', text, re.DOTALL).group(1).strip()
        return sql_code
    
    async def _extract_sql_async(self, text):
        print(text)
        print(type(text))
        sql_code = re.search(r'```sql(.*?)```', text, re.DOTALL).group(1).strip()
        return sql_code
    
    def send_message(self, 
                    content: Union[str, Dict, MessageContent], 
                    role: str, 
                    receiver: Optional[str] = None):
        try:
            # 内容转换
            if isinstance(content, MessageContent):
                msg_content = content
            elif isinstance(content, str):
                msg_content = MessageContent(text=content)
            elif isinstance(content, dict):
                if 'text' not in content:
                    raise ValueError("消息字典必须包含text字段")
                msg_content = MessageContent(**content)
            else:
                raise TypeError(f"无效内容类型: {type(content)}")

            # 创建消息
            message = Message(
                sent_from=self.name,
                role=role,
                content=msg_content,
                send_to=receiver
            )
            
            # 提交到队列
            self.mq.add_message(message)
            
        except Exception as e:
            print(f"[{self.name}] 消息发送失败: {str(e)}")