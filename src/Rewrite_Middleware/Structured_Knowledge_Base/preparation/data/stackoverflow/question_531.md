# is it a bad idea to write down too many methods inside adapter?
[Link to question](https://stackoverflow.com/questions/30162477/is-it-a-bad-idea-to-write-down-too-many-methods-inside-adapter)
**Creation Date:** 1431331538
**Score:** 0
**Tags:** java, android, android-alertdialog
## Question Body
<p>I am using RecyclerView to populate my CardView. Inside CardView, upon clicking on each card, I want to show a custom AlertDialog box with 4 fields. Once user fill those up and submit, I update my database.</p>

<p>Everything is working properly now. Only thing is, all these methods (AlerDialog, query database etc.) I used are inside my RecyclerView Adapter.</p>

<p>Upon reading some posts here in SO, i saw several people suggested against it, e.g. not to right down these kind of methods (specially Dialog) inside Adapter. So, my question is, whether i should rewrite my code or it is all the same performance-wise?</p>

<p>Below is part of my adapter:</p>

<pre><code>public class CardHolderAdapter extends RecyclerView.Adapter&lt;CardHolderAdapter.CardViewHolder&gt;{    

    ====== CONSTRUCTOR ========

    ====== VIEW HOLDER ========

    ====== onCreateViewHolder METHOD ========

    @Override
    public void onBindViewHolder(CardHolderAdapter.CardViewHolder holder, final int position) {
        holder.textViewBookname.setText(cardHolderList.get(position).getTitle());
        ...............
        ...............
        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                alertDialogWishlist(String ... args).show();
            }
        });
    }

    @Override
    public int getItemCount() {
        return cardHolderList.size();
    }

    public Dialog alertDialogWishlist(String ... args){
        AlertDialog.Builder myDialog = new AlertDialog.Builder(context);
        View layout = LayoutInflater.from((ActivityMyList) context).inflate(R.layout.alert_dialog_mylist_wishlist, null);

        // DATABASE QUERY TO FETCH CUSTOM FIELDS VALUES (4 FILEDS IN TOTAL)

        layout.findViewById(R.id.field1).setText(val1)
        .....................
        .....................

        myDialog.setView(layout)
                .setTitle(title)
                .setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.cancel();
                    }
                })
                .setPositiveButton(title, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        // DATABASE CONNECTION TO UPDATE NEW VALUES
                    }
                });
        return myDialog.create();
    }
}
</code></pre>

## Answers
### Answer ID: 30164268
<ol>
<li>There's no performance hit.</li>
</ol>

<p>There's no direct performance hit to putting methods in your adapter class.  This is a java class, like any other, that just implements the necessary classes for it to function as an adapter.  Whether you put your dialog creator / database lookups, in their own class, in the activity, or leave them in the adapter....doesn't matter performance wise.</p>

<ol start="2">
<li>Cache database results.</li>
</ol>

<p>That said, adapter methods get called frequently.  Scrolling a listView adapter for instance would create dozens of calls to create the child views, and if you wrap database calls in one of these heavily called methods it could very well hang.  There are things you can do to solve this problem like caching database values, using a single lookup, etc...</p>

<ol start="3">
<li>Moving methods out of the class is about access and modular design.</li>
</ol>

<p>If other things are going to be calling the database, and the logic is not unique to the adapter, it should be placed in an area where other class methods can access it without needing to have an instance of adapter or even having the adapter class as part of the project. </p>

