# How to set OnClickLitsener to Button in Listview
[Link to question](https://stackoverflow.com/questions/8403574/how-to-set-onclicklitsener-to-button-in-listview)
**Creation Date:** 1323189969
**Score:** 0
**Tags:** android, listview, adapter
## Question Body
<p>I now have a listview using simplecursoradapter to get data from the database and I query a link from the database and assign it to a button in each row of the list and I am rewriting the simplecursoradapter class to set onclicklistener for the button, but my codes aren't working, would anyone tell me what's the problem? thx</p>

<p>this is my Adapter</p>

<pre><code>public class ChannelAdapter extends SimpleCursorAdapter{

    private LayoutInflater mInflater;
    private List&lt;ChannelPoster&gt; items;
    private Context mContext;
    private String dblink;

    public ChannelAdapter(Context context, int layout, Cursor c, String[] from,
            int[] to) {
        super(context, layout, c, from, to);
        // TODO Auto-generated constructor stub
    }

    @Override
    public View getView(int position,View convertView,ViewGroup par)
    {
      ViewHolder holder;

      if(convertView == null)
      {

        convertView = mInflater.inflate(R.layout.channelview, null);

        holder = new ViewHolder();
        holder.image = (ImageView) convertView.findViewById(R.id.poster);
        holder.text = (TextView) convertView.findViewById(R.id.channel); 
        holder.button = (ImageButton) convertView.findViewById(R.id.douban);
        convertView.setTag(holder);

      }
      else
      {
        holder = (ViewHolder) convertView.getTag();
      }

      ChannelPoster tmpN=(ChannelPoster)items.get(position);

      holder.text.setText(tmpN.getChannel());
      holder.image.setImageResource(tmpN.getPoster());
      holder.button.setOnClickListener(new ImageButton.OnClickListener() 
      {
      public void onClick(View v) 
      {
        // TODO Auto-generated method stub 

          Intent intent = new Intent();
          intent.setClass(mContext, Doubanframe.class);
          Bundle bunde = new Bundle();
          bunde.putString("dblink",dblink);
          intent.putExtras(bunde);
          mContext.startActivity(intent);

            } 

      });
      return convertView;
    }


    private class ViewHolder
    {
    ImageView image;
    TextView text;
    ImageButton button;
    }
  }
</code></pre>

<p>and this is how I populate the listview</p>

<pre><code>mDB = new ChannelDB(this);

        String[] columns = {mDB.KEY_ID, mDB.KEY_POSTER, mDB.KEY_CHANNEL, mDB.KEY_PATH, mDB.KEY_DBLINK};
        String   table   = mDB.channelS_TABLE;

        c = mDB.getHandle().query(table, columns, null, null, null, null, null);

        startManagingCursor(c);

        SimpleCursorAdapter adapter = new SimpleCursorAdapter(this,
                R.layout.channelview,
                c,
                new String[] {mDB.KEY_POSTER, mDB.KEY_CHANNEL, mDB.KEY_DBLINK},
                new int[] { R.id.poster, R.id.channel, R.id.douban});

        channellist.setAdapter(adapter);
</code></pre>

## Answers
### Answer ID: 8409547
<p>I have solved this problem using the method in</p>

<p><a href="https://stackoverflow.com/questions/1709166/android-listview-elements-with-multiple-clickable-buttons">Android: ListView elements with multiple clickable buttons</a></p>

<p>in case someone wants to know</p>

### Answer ID: 8404273
<pre><code>public class ChannelAdapter extends SimpleCursorAdapter implements OnClickListener {

@Override
                public void onClick(View view) {
                       public void onClick(View view) {

                int view_id = view.getId();
                Log.d(THIS_FILE, "Im clicked....");



                switch (view_id) {

                case R.id.douban: {
                        dialFeedback.giveFeedback(ToneGenerator.TONE_DTMF_0);
                        keyPressed(KeyEvent.KEYCODE_0);
                        break;
                }
                }
}





}
</code></pre>

### Answer ID: 8403843
<p>try android.view.View.OnClickListener instead</p>

<pre><code>@Override
public View getView(int position,View convertView,ViewGroup par)
{
  ViewHolder holder;

  if(convertView == null)
  {

    convertView = mInflater.inflate(R.layout.channelview, null);

    holder = new ViewHolder();
    holder.image = (ImageView) convertView.findViewById(R.id.poster);
    holder.text = (TextView) convertView.findViewById(R.id.channel); 
    holder.button = (ImageButton) convertView.findViewById(R.id.douban);
     holder.button.setOnClickListener(new android.view.View.OnClickListener() 
  {
  public void onClick(View v) 
  {
    // TODO Auto-generated method stub 

      Intent intent = new Intent();
      intent.setClass(mContext, Doubanframe.class);
      Bundle bunde = new Bundle();
      bunde.putString("dblink",dblink);
      intent.putExtras(bunde);
      mContext.startActivity(intent);

        } 

  });        

    convertView.setTag(holder);

  }
  else
  {
    holder = (ViewHolder) convertView.getTag();
  }

  ChannelPoster tmpN=(ChannelPoster)items.get(position);

  holder.text.setText(tmpN.getChannel());
  holder.image.setImageResource(tmpN.getPoster());
  return convertView;
}
</code></pre>

