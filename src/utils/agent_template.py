"""
Author: Yuyang Song
Created: 2024-10-19
Last Modified: 2025-07-22

Module: agent_template.py

This module provides a comprehensive multi-agent communication framework with memory management,
message queuing, and observation patterns. It includes sliding window memory, message deduplication,
and flexible agent interaction capabilities.

Usage:
    # Initialize message queue and GPT client
    gpt = GPT(api_key="your-key", model="gpt-4o", base_url="https://api.openai.com/v1")
    message_queue = MessageQueue(window_size=10)
    
    # Create agents
    agent1 = Agent("Agent1", message_queue, gpt)
    agent2 = Agent("Agent2", message_queue, gpt)
    
    # Set up observation
    agent1.watch(["Agent2"])
    
    # Send messages
    agent1.send_message("Hello, Agent2!", "user", "Agent2")
"""

import re
import sys
from typing import List, Dict, Set, Optional, Union
from collections import deque, defaultdict
from time import perf_counter  
from dataclasses import dataclass
from pydantic import BaseModel
from dataclasses import replace

sys.path.append('../')
sys.path.append('./')

from src.utils.llm_client import GPT
    
class MessageContent(BaseModel):
    """
    Unified message content structure.
    """
    timestamp: float = perf_counter()  # High-precision
    text: str
    # metadata: Dict = {}

@dataclass
class Message:
    """
    Core message structure for agent communication.
    
    Represents a message sent between agents with metadata including sender,
    receiver, role, content, and timestamp information.
    """
    sent_from: str
    role: str
    content: MessageContent  
    send_to: Optional[str] = None
    timestamp: float = perf_counter() 

    def __post_init__(self):
        """
        Post-initialization processing to ensure content is properly formatted.
        
        Converts dict content to MessageContent instances and validates content type.
        
        Raises:
            ValueError: If content type is invalid
        """
        if isinstance(self.content, dict):
            self.content = MessageContent(**self.content)
        elif not isinstance(self.content, MessageContent):
            raise ValueError("Invalid content type, must be MessageContent or dict")

class MemoryWindow:
    """
    Sliding window memory container for efficient message storage.
    
    Maintains a fixed-size window of recent messages with sender-based indexing
    for fast retrieval. Uses deque for O(1) append/pop operations.
    
    Attributes:
        max_size (int): Maximum number of messages to store
        window (deque): Main storage for messages in chronological order
        sender_index (defaultdict): Index by sender for quick filtering
    """
    def __init__(self, max_size: int = 5):
        """
        Initialize memory window with specified capacity.
        
        Args:
            max_size (int): Maximum number of messages to store. Defaults to 5.
        """
        self.max_size = max_size
        self.window = deque(maxlen=max_size)
        # Maintain sender-based index for efficient filtering
        self.sender_index = defaultdict(lambda: deque(maxlen=max_size))

    def add(self, message: Message):
        """
        Add a message to the memory window.
        """
        self.window.append(message)
        self.sender_index[message.sent_from].append(message)

    def get_recent(self, k: int) -> List[Message]:
        """
        Retrieve the k most recent messages.
        """
        return list(self.window)[-k:] if k > 0 else list(self.window)

    def get_by_sender(self, sender: str, k: int) -> List[Message]:
        """
        Retrieve recent messages from a specific sender.
        """
        return list(self.sender_index.get(sender, deque()))[-k:]

class MessageQueue:
    """
    Enhanced message queue system with observation patterns and memory management.
    
    Attributes:
        full_history (List[Message]): Complete message history
        memory_window (MemoryWindow): Sliding window for recent messages
        observation_graph (defaultdict): Maps observed agents to observers
        reverse_observation_index (defaultdict): Maps observers to observed agents
        registered_agents (set): Set of registered agent names
        seen_messages (set): Set of message hashes for deduplication
    """
    def __init__(self, window_size: int = 10):
        """
        Initialize message queue with specified window size.
        
        Args:
            window_size (int): Size of sliding memory window. Defaults to 10.
        """
        # Complete message history
        self.full_history = []
        # Sliding memory window for recent messages
        self.memory_window = MemoryWindow(window_size)
        # Observation relationships
        self.observation_graph = defaultdict(set)
        # Reverse index for observers
        self.reverse_observation_index = defaultdict(set)
        self.registered_agents = set()  # Agent registration set
        self.seen_messages = set()  # Deduplication set
    
    def register_agent(self, name: str):
        self.registered_agents.add(name)
    
    def _add_copy(self, message: Message):
        """
        Safely add a message copy with deduplication.
        
        Creates a hash based on sender, content, and receiver to prevent
        duplicate messages in the memory window.
        """
        copy_hash = hash((
            message.sent_from, 
            message.content.text,
            message.send_to  # Include receiver in hash to differentiate messages
        ))
        if copy_hash not in self.seen_messages:
            self.memory_window.add(message)
            self.seen_messages.add(copy_hash)

    def add_message(self, message: Message):
        """
        Add a message to the queue with proper routing and observation handling.
        
        Handles different message types:
        - Self-messages (sender == receiver)
        - Broadcast messages (send_to == "all")
        - Direct messages with observer notifications
        """

        # Handle self-messages
        if message.send_to == message.sent_from:
            self._add_copy(message)
            return

        # Handle broadcast messages
        if message.send_to == "all":
            self.full_history.append(message)  # Store in full history
            broadcast_msg = replace(message, send_to="all")
            self._add_copy(broadcast_msg)
            return

        # Handle regular messages with deduplication
        unique_hash = hash((message.sent_from, message.content.text, message.send_to))
        if unique_hash in self.seen_messages:
            return
        
        self.full_history.append(message)
        self.memory_window.add(message)
        self.seen_messages.add(unique_hash)

        # Process observer notifications
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
        """
        Establish observation relationship between agents.
        """
        self.observation_graph[target].add(observer)
        self.reverse_observation_index[observer].add(target)

    def get_memories(self, 
                    observer: Optional[str] = None,
                    k: int = 5,
                    strategy: str = 'recent') -> List[Message]:
        """
        Retrieve memories with flexible filtering strategies.
        
        Supports multiple retrieval strategies and combines messages from:
        - Observed agents (via observation relationships)
        - Direct messages to the observer
        - Broadcast messages
        """
        if not observer:
            return self.memory_window.get_recent(k)

        targets = self.reverse_observation_index.get(observer, set())
        observed_messages = []

        # Get messages from observed target
        if strategy == 'per_sender':
            observed_messages = self._get_per_sender_memories(targets, observer, k)
        elif strategy == 'recent':
            observed_messages = self._get_recent_memories(targets, observer, k)
        else:
            observed_messages = []

        # Get direct messages to observer (including self-messages)
        direct_messages = [
            msg for msg in self.memory_window.get_recent(2*k)
            if msg.send_to == observer
        ]

        # Get broadcast messages
        broadcast_messages = [
            msg for msg in self.memory_window.get_recent(2*k)
            if msg.send_to == "all"
        ]
        
        combined = sorted(
        [(i, msg) for i, msg in enumerate(observed_messages + broadcast_messages + direct_messages)],
        key=lambda x: (x[1].timestamp, -x[0]),  # Timestamp first, then insertion order
        reverse=True
        )
        unique_messages = [msg for _, msg in combined][:k]
        
        return unique_messages[:k]

    def _get_per_sender_memories(self, targets: Set[str], observer: str, k: int) -> List[Message]:
        """
        Get recent messages from each target sender.
        
        Retrieves up to k messages from each observed target where the
        receiver is either the observer or "all" (broadcast).
        """
        results = []
        for target in targets:
            messages = self.memory_window.get_by_sender(target, k*2)
            filtered = [
                msg for msg in messages
                if msg.send_to in {observer, "all"}  # Observer or broadcast
            ]
            results.extend(filtered[:k])
        return sorted(results, key=lambda x: x.timestamp, reverse=True)[:k]

    def _get_recent_memories(self, targets: Set[str], observer: str, k: int) -> List[Message]:
        """
        Get most recent messages from all targets combined.
        """
        candidates = [
            msg for msg in self.memory_window.get_recent(k*2)
            if msg.sent_from in targets and msg.send_to in {observer, "all"}
        ]
        return candidates[-k:]
    


class Agent:
    """
    Enhanced Agent base class for multi-agent systems.
    
    Attributes:
        name (str): Unique identifier for the agent
        llm (GPT): Language model client for AI capabilities
        mq (MessageQueue): Shared message queue for communication
        observation_strategy (str): Default memory retrieval strategy
    """
    def __init__(self, name: str, message_queue: MessageQueue, gpt: GPT):
        """
        Initialize agent with communication and AI capabilities.
        
        Args:
            name (str): Unique name for the agent
            message_queue (MessageQueue): Shared message queue system
            gpt (GPT): GPT client for language model interactions
        """
        self.name = name
        self.llm = gpt  
        self.mq = message_queue
        self.mq.register_agent(name)  # Register in the system
        self.observation_strategy = 'per_sender'  # Default observation strategy

    def watch(self, targets: List[str]):
        """
        Establish observation relationships with target agents.
        
        Args:
            targets (List[str]): List of agent names to observe
        """
        for target in targets:
            self.mq.watch_agent(target, self.name)

    def retrieve_memories(self, k: int = 5, strategy: Optional[str] = None) -> List[Message]:
        """
        Retrieve relevant memories using specified strategy.
        
        Args:
            k (int): Maximum number of messages to retrieve. Defaults to 5.
            strategy (Optional[str]): Override default observation strategy
            
        Returns:
            List[Message]: List of relevant messages
        """
        return self.mq.get_memories(
            observer=self.name,
            k=k,
            strategy=strategy if strategy is not None else self.observation_strategy
        )

    
    def format_memories(self, messages: List[Message]) -> str:
        """
        Format messages into a readable string representation.
        
        Creates a formatted string showing message flow with timestamps,
        sender/receiver information, and content.
    
        """
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
            # Content type conversion
            if isinstance(content, MessageContent):
                msg_content = content
            elif isinstance(content, str):
                msg_content = MessageContent(text=content)
            elif isinstance(content, dict):
                if 'text' not in content:
                    raise ValueError("Message dict must contain 'text' field")
                msg_content = MessageContent(**content)
            else:
                raise TypeError(f"[{self.name}] Message sending failed: {str(e)}")

            # Create message instance
            message = Message(
                sent_from=self.name,
                role=role,
                content=msg_content,
                send_to=receiver
            )
            
            # Send message to the queue
            self.mq.add_message(message)
            
        except Exception as e:
            print(f"[{self.name}] Message sending failed: {str(e)}")


# # Example usage and testing

# # Example setup (commented out by default)
# gpt = GPT(api_key="your-key", model="gpt-4o", base_url="https://api.openai.com/v1")
# message_queue = MessageQueue(window_size=10)

# # Create agents
# agent1 = Agent("Agent1", message_queue, gpt)
# agent2 = Agent("Agent2", message_queue, gpt)

# # Set up observation
# agent1.watch(["Agent2"])

# # Send messages
# agent1.send_message("Hello, Agent2!", "user", "Agent2")
# agent2.send_message("Hello back!", "assistant", "Agent1")

# # Retrieve and display memories
# memories = agent1.retrieve_memories(k=5)
# formatted = agent1.format_memories(memories)
# print(formatted)