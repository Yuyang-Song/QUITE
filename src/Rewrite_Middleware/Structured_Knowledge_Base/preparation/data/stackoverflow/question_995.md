# How do I prevent user data from typing again firebase database?
[Link to question](https://stackoverflow.com/questions/53805077/how-do-i-prevent-user-data-from-typing-again-firebase-database)
**Creation Date:** 1544983727
**Score:** 0
**Tags:** android, firebase, firebase-realtime-database, firebase-authentication
## Question Body
<p>Each time the activity is called, it writes again. But I don't want him rewriting the premium part. How do I check the user ID to not rewrite the database? How do I query the user's identity in the database ?</p>

<pre><code> public void writeFirebase() {
        Users users = new Users();
        if (mUser.getPhotoUrl() != null) {
            users.setUserProfilPic(mUser.getPhotoUrl().toString());
        }
        if (mUser.getDisplayName() != null) {
            users.setUserName(mUser.getDisplayName());
        }
        users.setUserId(mUser.getUid());
        users.setUserPremium("false");
        users.setUserPremiumDate("");
        users.setUserEmail(mUser.getEmail());

        myRef.child("Users").child(users.getUserId()).setValue(users);

    }
</code></pre>

## Answers
### Answer ID: 53805340
<p>If you want to check that the data is not already present or not for the particular userID, you need to know the user ID.</p>

<p>For fetching user by ID :</p>

<pre><code>ValueEventListener userListener = new ValueEventListener() {
@Override
public void onDataChange(DataSnapshot dataSnapshot) {
    // Get Post object and use the values to update the UI
    User user = dataSnapshot.getValue(User.class);

    // **HERE YOU CAN CHECK IF THE PREMIUM VALUE HAS BEEN SET OR NOT**

}

@Override
public void onCancelled(DatabaseError databaseError) {
    // Getting Post failed, log a message
    Log.w(TAG, "loadPost:onCancelled", databaseError.toException());
    // ...
}
};
myRef.child("Users").child(yourUserID).addListenerForSingleValueEvent(userListener);
</code></pre>

<p>You can get more details here : <a href="https://firebase.google.com/docs/database/android/read-and-write#read_data_once" rel="nofollow noreferrer">https://firebase.google.com/docs/database/android/read-and-write#read_data_once</a></p>

