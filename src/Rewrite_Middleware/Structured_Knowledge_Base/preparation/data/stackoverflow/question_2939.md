# Room get the next Row(Item) in Android
[Link to question](https://stackoverflow.com/questions/59483822/room-get-the-next-rowitem-in-android)
**Creation Date:** 1577334360
**Score:** 0
**Tags:** android, sqlite, android-room
## Question Body
<p>Hi I am new to the Android room library, Ok I have a working program that display Notes and uses the Android Room components.
I am not searching for an Exact source code any suggestion or general guidance is fine with regards to this. </p>

<p>So I have a Class Note, A DAO class, A repository class, the database class, the ViewModel, an Adapter for a list view. The interface has a main activity and two fragments, the fist fragment displays list of notes and in EditNote Fragment where we are displaying just one note in details. This is correct <a href="http://developer.android.com/topic/libraries/architecture/adding-components" rel="nofollow noreferrer">with regards to the google documentation.</a></p>

<p>Everything is good and when I click an element of the list I get the EditNote 
 Fragment.  </p>

<p>All the code is exactly as shown in <a href="https://codinginflow.com/tutorials/android/room-viewmodel-livedata-recyclerview-mvvm/part-10-listadapter" rel="nofollow noreferrer">this tutorial</a></p>

<p>Now I want to add a Navigation button next in the EditNote Fragment. </p>

<ul>
<li>In the detail Fragment we get the Note class from the construcor and I am setting some vars  in the oncreatedview event by overriding it and getting the ViewModel to set up the observer that will trigger the OnChange.</li>
</ul>

<p>From what I read I need to change the current note (selected Row in the table) to trigger this OnChange event to display the next note (next row)
So : if we click on the next button we display the next Note row element, and by clicking on previous we display the previous note element.</p>

<ul>
<li><p><strong>Do I have to rewrite everything to the Dao Level with a query where I input the current note ID to get the next Note ? (can i do it using SQL?)</strong></p></li>
<li><p><strong>Does this room component system have an option to get the current row and change it?</strong>
<a href="https://i.sstatic.net/hjXKR.jpg" rel="nofollow noreferrer"><img src="https://i.sstatic.net/hjXKR.jpg" alt="enter image description here"></a></p></li>
</ul>

