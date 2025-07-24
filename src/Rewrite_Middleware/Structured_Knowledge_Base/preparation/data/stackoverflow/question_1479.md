# Can&#39;t add an item to room database
[Link to question](https://stackoverflow.com/questions/77834527/cant-add-an-item-to-room-database)
**Creation Date:** 1705513694
**Score:** 1
**Tags:** android, kotlin, mvvm, android-jetpack-compose, android-room
## Question Body
<p>For some reason I can't add an Item to room database , The rest of my Daos are working ok but it seems @Upsert isn't (obviously I'm messing up somewhere). I used the query in &quot;App inspection&quot; to add elements to it and successively viewed what was added making it obvious where the problem was.</p>
<p>The app is a simple app that stores memorised verses. Your help will be highly appreciated.</p>
<p>Daos</p>
<pre><code>interface DaoFunctions {

    @Upsert
    suspend fun addVerse(verse: Verse)


    @Query(&quot;SELECT * FROM MyVersesTable ORDER BY bookPosition ASC&quot;)
    fun getVerseByBook(): PagingSource&lt;Int,Verse&gt;

    @Query(&quot;SELECT * FROM MyVersesTable ORDER BY themeName ASC&quot;)
    fun getVersesByTheme(): PagingSource&lt;Int,Verse&gt;

    @Query(&quot;SELECT * FROM MyVersesTable ORDER BY date ASC&quot;)
    fun getVersesByDate(): PagingSource&lt;Int,Verse&gt;

    @Query(&quot;SELECT * FROM MyVersesTable&quot;)
    fun getVersesByDateFlow(): List&lt;Verse&gt;

    @Delete
     fun deletVerse(verse: Verse)




} 
</code></pre>
<p>Repository Interface</p>
<pre><code>interface DataBaseRepository {


    suspend fun addVerse(verse: Verse)

    fun getVerseByBook(): PagingSource&lt;Int, Verse&gt;

    fun getVersesByTheme(): PagingSource&lt;Int,Verse&gt;

    fun getVersesByDate(): PagingSource&lt;Int,Verse&gt;

    fun deletVerse(verse: Verse)

    fun getVersesByDateFlow(): List&lt;Verse&gt;

}  
</code></pre>
<p>Repository Implemented</p>
<pre><code>
class DataBaseRepositoryImpl @Inject constructor( val daos: DaoFunctions): DataBaseRepository{

    override suspend fun addVerse(verse: Verse)  = daos.addVerse(verse)

    override fun getVerseByBook() = daos.getVerseByBook()


    override fun getVersesByTheme() = daos.getVersesByTheme()

    override fun getVersesByDate() = daos.getVersesByDate()

    override fun deletVerse(verse: Verse) = daos.deletVerse(verse)

    override fun getVersesByDateFlow() = daos.getVersesByDateFlow()




}
</code></pre>
<p>Table</p>
<pre><code>
@Entity(tableName = &quot;MyVersesTable&quot;)
data class Verse(

    val verse: String,
    val bookName: String,
    val chapterAndVerseNumber: String,

    val bookPosition: Byte,
    val date: Long,


    val themeName: String,

    val photoFilePath: String,




    @PrimaryKey(autoGenerate = true)
    val id: Int = 0
)
</code></pre>
<p>Adding Verse View Model</p>
<pre><code>
@HiltViewModel
class AddingVerseScreenViewModel @Inject constructor(

    private val daoFunctions: DataBaseRepositoryImpl

): ViewModel() {





    private val _state = MutableStateFlow(AddingVerseScreenStates())
    val state = _state.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), AddingVerseScreenStates())


    private val eventsChannel = Channel&lt;AddingVerseScreenEvents&gt;()
    val eventFlow =  eventsChannel.receiveAsFlow()


    fun triggerSaveVerseEvent(){

        viewModelScope.launch {

            eventsChannel.send(AddingVerseScreenEvents.saveVerse)

        }

    }


    fun triggerShowingPopUpMenuEvent(){

        viewModelScope.launch {

            eventsChannel.send(AddingVerseScreenEvents.showPopUpMenu)

        }

    }





    fun triggerHidingPopUpMenuEvent(){

        viewModelScope.launch {

            eventsChannel.send(AddingVerseScreenEvents.hidePopUpMenu)

        }

    }







    fun saveVerse() {

//        if (_state.value.bookName.isBlank() || _state.value.verse.isBlank() || _state.value.themeName.isBlank() || _state.value.photoFilePath.isBlank() || _state.value.note.isBlank())
//            return


        val verse =  Verse(
            bookName = _state.value.bookName,
            chapterAndVerseNumber = _state.value.chapter + &quot;:&quot; + _state.value.verseNumber,
            verse = _state.value.verse,
            date = System.currentTimeMillis(),
            themeName = _state.value.themeName,
            bookPosition = _state.value.bookPosition,
            photoFilePath = _state.value.photoFilePath,


        ) // VERSE ENDS

        viewModelScope.launch {


            daoFunctions.addVerse(verse)

        } // SCOPE ENDS


//        _state.update {
//
//            it.copy(
//
//                bookName = &quot;&quot;,
//                chapterAndVerseNumber = &quot;&quot;,
//                verse = &quot;&quot;,
//                bookPosition = 0,
//
//                note = &quot;&quot;,
//
//                themeName = &quot;&quot;,
//                themeColour = &quot;&quot;,
//
//                photoFilePath = &quot;&quot;,
//
//            ) // COPY ENDS
//
//        } // UPDATE ENDS





    }







    fun showPopUpMenu(){


        _state.update { it.copy(showingPopupMenu = true) }


    }

    fun hidePopUpMenu(){


        _state.update {    it.copy(showingPopupMenu = false)    }


    }



    fun setBookName(book: String){

        _state.update {    it.copy(bookName = book)     }


    }



    fun showBookSelectionDialog(){

        _state.update {    it.copy(isBookSelectionDialogShowing = true)     }
    }





    fun hideBookSelectionDialog(){

        _state.update {    it.copy(isBookSelectionDialogShowing = false)     }
    }







    fun showChapterSelectionDialog(){

        _state.update {    it.copy(isChapterSelectionDialogShowing = true)     }
    }





    fun hideChapterSelectionDialog(){

        _state.update {    it.copy(isChapterSelectionDialogShowing = false)     }
    }




    fun showVerseSelectionDialog(){

        _state.update {    it.copy(isVerseSelectionDialogShowing = true)     }
    }





    fun hideVerseSelectionDialog(){

        _state.update {    it.copy(isVerseSelectionDialogShowing = false)     }
    }






    fun setChapter(chapter: String){

        _state.update {    it.copy(chapter = chapter)     }

    }







    fun setVerseNumber(verseNumber: String){

        _state.update {    it.copy(verseNumber = verseNumber)     }

    }





    fun setVerse(verse: String){

        _state.update {    it.copy(verse = verse)     }

    }


    fun setNote(note: String){

        _state.update {    it.copy(note = note)     }
    }


    fun setThemeName(themeName: String){

        _state.update {    it.copy(themeName = themeName)     }

    }


    fun setThemeColour(colour: String){

        _state.update {    it.copy(themeColour = colour)     }

    }


    fun setPhotoFilePath(path: String){

        _state.update {    it.copy(photoFilePath = path)     }

    }



    fun setConditionForThemeExistence(condition: Boolean){

        _state.update {    it.copy(doesThemeExist = condition)     }
    }


















}
</code></pre>
<p>Home Screen View Model</p>
<pre><code>@HiltViewModel
class HomeScreenViewModel @Inject constructor(

    val daoFunctions: DataBaseRepositoryImpl

): ViewModel() {




  private val _state = MutableStateFlow(HomeScreenStates())


  val state = _state.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), HomeScreenStates())


    val allVerses = Pager(

     config = PagingConfig(

         pageSize = 60,
         enablePlaceholders = true,
         maxSize = 200

     ) // PAGING CONFIG ENDS
 ) {

//      when(_state.value.sortType){
//
//          SortType.byBook -&gt; daoFunctions.getVerseByBook()
//          SortType.byDate -&gt; daoFunctions.getVersesByDate()
//          SortType.byTheme -&gt; daoFunctions.getVersesByTheme()
//      }



            daoFunctions.getVersesByDate()



 }// PAGER ENDS


    private val eventsChannel = Channel&lt;HomeScreenEvents&gt;()
    val eventFlow = eventsChannel.receiveAsFlow()


    fun triggerShowingPopUpMenuEvent(){

         viewModelScope.launch {

             eventsChannel.send(HomeScreenEvents.showPopUpMenu)

         }

    }





    fun triggerHidingPopUpMenuEvent(){

        viewModelScope.launch {

            eventsChannel.send(HomeScreenEvents.hidePopUpMenu)

        }

    }






    fun triggerShowingMenuSideBarEvent(){

        viewModelScope.launch {

            eventsChannel.send(HomeScreenEvents.showMenuSideBar)

        }

    }





    fun triggerHidingMenuSideBarEvent(){

        viewModelScope.launch {

            eventsChannel.send(HomeScreenEvents.hideMenuSideBar)

        }

    }






    fun triggerExpandingSearchBarEvent(){

        viewModelScope.launch {

            eventsChannel.send(HomeScreenEvents.expandSearchBar)

        }

    }





    fun triggerCollapsingSearchBarEvent(){

        viewModelScope.launch {

            eventsChannel.send(HomeScreenEvents.collapseSearchBar)

        }

    }







    fun triggerShowingAddVerseFloatingButton(){

        viewModelScope.launch {

            eventsChannel.send(HomeScreenEvents.showAddingVerseFloatingButton)

        }

    }





    fun triggerHidingAddVerseFloatingButton(){

        viewModelScope.launch {

            eventsChannel.send(HomeScreenEvents.showAddingVerseFloatingButton)

        }

    }






    fun triggerChangingSortTypeEvent(sortType: SortType){

        viewModelScope.launch {

            eventsChannel.send(HomeScreenEvents.changeSortTypeOfVersesTo(sortType))

        }


    }






















     fun showPopUpMenu(){


        _state.update { it.copy(showingPopupMenu = true) }


    }

    fun hidePopUpMenu(){


        _state.update {    it.copy(showingPopupMenu = false)    }


    }


    fun showMenuSideBar(){

        _state.update {     it.copy(showingMenuSideBar = false)    }

    }


    fun hideMenuSideBar(){

        _state.update {     it.copy(showingMenuSideBar = false)     }

    }


    fun expandSearchBar(){

        _state.update {      it.copy(expandedSearchBar = true)     }

    }


    fun collapseSearchBar(){

        _state.update {      it.copy(expandedSearchBar = false)     }

    }



    fun showAddingVerseFloatingButton(){

        _state.update {      it.copy(showingAddingVerseFloatingButton = true)     }

    }

    fun hideAddingVerseFloatingButton(){

        _state.update {      it.copy(showingAddingVerseFloatingButton = false)     }

    }



    fun changeSortTypeOfVersesTo(sortType: SortType){


        _state.update {      it.copy(sortType =  sortType)     }

    }


    fun updateUiThemeTo(theme: String){


        _state.update {      it.copy(lastOpenedTheme = theme)     }

    }



}

</code></pre>
<p>Gradle Module code</p>
<pre><code>plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
    id 'kotlin-kapt'
    id 'com.google.dagger.hilt.android'
}

apply plugin: 'com.android.application'
apply plugin: 'com.google.dagger.hilt.android'

android {
    namespace 'com.example.Sword'
    compileSdk 34

    defaultConfig {
        applicationId &quot;com.example.Sword&quot;
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName &quot;1.0&quot;

        testInstrumentationRunner &quot;androidx.test.runner.AndroidJUnitRunner&quot;
        vectorDrawables {
            useSupportLibrary true
        }
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = '1.8'


    }
    buildFeatures {
        compose true
    }
    composeOptions {
        kotlinCompilerExtensionVersion '1.5.4'
    }
    packagingOptions {
        resources {
            excludes += '/META-INF/{AL2.0,LGPL2.1}'
        }
    }
}

dependencies {

    implementation 'androidx.core:core-ktx:1.8.0'
    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.3.1'
    implementation 'androidx.activity:activity-compose:1.5.1'
    implementation platform('androidx.compose:compose-bom:2022.10.00')
    implementation 'androidx.compose.ui:ui'
    implementation 'androidx.compose.ui:ui-graphics'
    implementation 'androidx.compose.ui:ui-tooling-preview'
    implementation 'androidx.compose.material3:material3'
    implementation platform('androidx.compose:compose-bom:2023.03.00')
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
    androidTestImplementation platform('androidx.compose:compose-bom:2022.10.00')
    androidTestImplementation 'androidx.compose.ui:ui-test-junit4'
    androidTestImplementation platform('androidx.compose:compose-bom:2023.03.00')
    debugImplementation 'androidx.compose.ui:ui-tooling'
    debugImplementation 'androidx.compose.ui:ui-test-manifest'

    // ViewModel Compose
    implementation &quot;androidx.lifecycle:lifecycle-viewmodel-compose:2.4.1&quot;

     //FOR ROOM
    implementation &quot;androidx.room:room-ktx:2.5.2&quot;
    implementation(&quot;androidx.room:room-paging:2.5.2&quot;)
    kapt &quot;androidx.room:room-compiler:2.5.2&quot;


//    //Dagger - Hilt
//    implementation &quot;com.google.dagger:daggerHilt-android:2.40.5&quot;
//    kapt &quot;com.google.dagger:daggerHilt-android-compiler:2.40.5&quot;
//    implementation &quot;androidx.daggerHilt:daggerHilt-lifecycle-viewmodel:1.0.0-alpha03&quot;
//    kapt &quot;androidx.daggerHilt:daggerHilt-compiler:1.0.0&quot;
//    implementation 'androidx.daggerHilt:daggerHilt-navigation-compose:1.0.0'
//    //


    //HILT
    implementation 'com.google.dagger:hilt-android:2.49'
    kapt 'com.google.dagger:hilt-compiler:2.49'
    implementation 'androidx.fragment:fragment-ktx:1.6.2'


    // For instrumentation tests
    androidTestImplementation  'com.google.dagger:hilt-android-testing:2.49'
    kaptAndroidTest 'com.google.dagger:hilt-compiler:2.49'

    // For local unit tests
    testImplementation 'com.google.dagger:hilt-android-testing:2.49'
    kaptTest 'com.google.dagger:hilt-compiler:2.49'



    //PAGER
    def paging_version = &quot;3.2.1&quot;

    implementation &quot;androidx.paging:paging-runtime:$paging_version&quot;

    // alternatively - without Android dependencies for tests
    testImplementation &quot;androidx.paging:paging-common:$paging_version&quot;
    
    // optional - Jetpack Compose integration
    implementation &quot;androidx.paging:paging-compose:3.3.0-alpha02&quot;

    // collect as state with lifecycle
    implementation(&quot;androidx.lifecycle:lifecycle-runtime-compose:2.6.2&quot;)



}

hilt {
    enableAggregatingTask = false
}

kapt {
    correctErrorTypes true
}

</code></pre>
<p>Gradle Project code</p>
<pre><code>// Top-level build file where you can add configuration options common to all sub-projects/modules.
buildscript {
    repositories {
        // other repositories...
        mavenCentral()
    }
    dependencies {
        // other plugins...
        classpath 'com.google.dagger:hilt-android-gradle-plugin:2.49'
    }
}



plugins {

    id 'com.google.dagger.hilt.android' version '2.49' apply false
    id 'com.android.application' version '8.1.2' apply false
    id 'com.android.library' version '8.1.2' apply false
    id 'org.jetbrains.kotlin.android' version '1.9.20' apply false

}

</code></pre>
<p>Tried everything I can think of, Rewriting everything, Double checking , EVEVERYTHING.</p>
<p>I'm using daggerhilt so my suspicion is that somehow the dao object is being shared to my screen where I view the items and not to the screen where I add the item</p>

## Answers
### Answer ID: 77835302
<p>I tried out your code.
The best and fast possible solution for this is.</p>
<ol>
<li><p>Updated Room version.
<a href="https://i.sstatic.net/XaUZL.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/XaUZL.png" alt="Diff screenshot" /></a></p>
</li>
<li><p>Removed return type Unit assignment for Dao method addVerse
<a href="https://i.sstatic.net/CM65b.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/CM65b.png" alt="enter image description here" /></a></p>
</li>
</ol>
<p><strong>Result</strong>
<a href="https://i.sstatic.net/UEQWu.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/UEQWu.png" alt="enter image description here" /></a></p>
<p>Reason: I read some posts on stackoverflow and reddit about it.
When I was trying to remove return type Unit assignment for Dao method addVerse without updating the room library then I was getting this error.
<strong>Type of the parameter must be a class annotated with @Entity or a collection/array of it</strong></p>
<p>I found out that there was an open issue for this :
<a href="https://stackoverflow.com/a/73304737/7613626">https://stackoverflow.com/a/73304737/7613626</a></p>

