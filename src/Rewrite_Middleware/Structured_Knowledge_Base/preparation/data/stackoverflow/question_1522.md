# How to set OnClickLitsener to Button in ListView with Override SimpleCursorAdapter
[Link to question](https://stackoverflow.com/questions/8402099/how-to-set-onclicklitsener-to-button-in-listview-with-override-simplecursoradapt)
**Creation Date:** 1323184166
**Score:** 2
**Tags:** android, listview, button, adapter
## Question Body
<p>I now have a listview using simplecursoradapter to get data from the database and I query a link from the database and assign it to a button in each row of the list and I am rewriting the simplecursoradapter class to set onclicklistener for the button, but my codes aren't working, would anyone tell me what's the problem?</p>

<p>This is my Adapter:</p>

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

<p>and this is how I populate the listview:</p>

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

<p>LogCat</p>

<pre><code>12-06 15:07:01.093: INFO/System.out(1257): debugger has settled (1375)
12-06 15:07:02.172: DEBUG/dalvikvm(1257): GC freed 884 objects / 61568 bytes in 118ms
12-06 15:07:03.029: DEBUG/Splash(1257): table exist
12-06 15:07:03.359: WARN/InputManagerService(59): Got RemoteException sending setActive(false) notification to pid 1225 uid 10028
12-06 15:07:03.903: INFO/ActivityManager(59): Displayed activity com.appkon.hdtvs/.Splash: 7947 ms (total 7947 ms)
12-06 15:07:04.920: INFO/ActivityManager(59): Starting activity: Intent { cmp=com.appkon.hdtvs/.HDtvs }
12-06 15:07:06.001: INFO/System.out(1257): resolveUri failed on bad bitmap uri: http://movie.douban.com/subject/5372374/
12-06 15:07:06.190: INFO/System.out(1257): resolveUri failed on bad bitmap uri: http://movie.douban.com/subject/3190880/
12-06 15:07:06.450: INFO/System.out(1257): resolveUri failed on bad bitmap uri: http://movie.douban.com/subject/3990470/
12-06 15:07:06.720: DEBUG/dalvikvm(1257): GC freed 546 objects / 27992 bytes in 107ms
12-06 15:07:06.780: INFO/System.out(1257): resolveUri failed on bad bitmap uri: http://movie.douban.com/subject/4804079/
12-06 15:07:06.931: INFO/System.out(1257): resolveUri failed on bad bitmap uri: http://movie.douban.com/subject/6557005/
12-06 15:07:07.111: INFO/System.out(1257): resolveUri failed on bad bitmap uri: http://movie.douban.com/subject/4317617/
12-06 15:07:07.270: INFO/System.out(1257): resolveUri failed on bad bitmap uri: http://movie.douban.com/subject/6436783/
12-06 15:07:07.410: INFO/System.out(1257): resolveUri failed on bad bitmap uri: http://movie.douban.com/subject/2156528/
12-06 15:07:07.590: INFO/System.out(1257): resolveUri failed on bad bitmap uri: http://movie.douban.com/subject/6778677/
</code></pre>

## Answers
### Answer ID: 9068704
<pre><code>@Override
    public View getView(int position, View convertView, ViewGroup parent) {
        View view = convertView;
        if (view == null)
            view = LayoutInflater.from(DummyListViewProjectActivity.this).inflate(R.layout.list_item, parent, false);
        TextView tv = (TextView) view.findViewById(R.id.text);
        tv.setText(adapterItems.get(position));
        Button bt = (Button) view.findViewById(R.id.button);
        bt.setText(adapterItems.get(position));
        bt.setTag(adapterItems.get(position));
        bt.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View v) {
                Toast.makeText(DummyListViewProjectActivity.this, v.getTag().toString(), Toast.LENGTH_SHORT).show();
            }
        });
        return view;
    }
</code></pre>

<p>it worked for me and did show the toast with different values. Can you try without the holder one's just for trying.</p>

