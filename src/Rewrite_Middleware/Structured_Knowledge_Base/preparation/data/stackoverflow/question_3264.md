# Why my room doesnt work properly in kotlin compose
[Link to question](https://stackoverflow.com/questions/74302738/why-my-room-doesnt-work-properly-in-kotlin-compose)
**Creation Date:** 1667476877
**Score:** 1
**Tags:** android, kotlin
## Question Body
<p>I've been working on dictionary app for a while in kotlin with compose. I want the user to be able to create their own dictionary as a feature of the application.I use the room database for this, I have done all the integrations, but I don't understand why it keeps getting errors. I checked everything but couldn't find where the problem is originating from. I will share my codes and errors.</p>
<p><strong>errors</strong></p>
<pre><code>error: Entities and POJOs must have a usable public constructor. You can have an empty constructor or a constructor whose parameters match the fields (by name and type). - kotlin.Unit
C:\Users\enest\AndroidStudioProjects\DictionaryApp\app\build\tmp\kapt3\stubs\debug\com\enestigli\dictionaryapp\data\locale\OwnDicDao.java:11: error: Not sure how to convert a Cursor to this method's return type (kotlin.Unit).
    public abstract java.lang.Object GetAllDictionary(@org.jetbrains.annotations.NotNull()
                                     ^
C:\Users\enest\AndroidStudioProjects\DictionaryApp\app\build\tmp\kapt3\stubs\debug\com\enestigli\dictionaryapp\data\locale\OwnDicDao.java:11: warning: The query returns some columns [dicName, creationTime, uid] which are not used by kotlin.Unit. You can use @ColumnInfo annotation on the fields to specify the mapping. You can annotate the method with @RewriteQueriesToDropUnusedColumns to direct Room to rewrite your query to avoid fetching unused columns.  You can suppress this warning by annotating the method with @SuppressWarnings(RoomWarnings.CURSOR_MISMATCH). Columns returned by the query: dicName, creationTime, uid. Fields in kotlin.Unit: .
    public abstract java.lang.Object GetAllDictionary(@org.jetbrains.annotations.NotNull()
                                     ^
C:\Users\enest\AndroidStudioProjects\DictionaryApp\app\build\tmp\kapt3\stubs\debug\com\enestigli\dictionaryapp\data\locale\OwnDicDao.java:33: error: Unused parameter: dicId
    public abstract java.lang.Object Update(@org.jetbrains.annotations.Nullable()
                                     ^
C:\Users\enest\AndroidStudioProjects\DictionaryApp\app\build\tmp\kapt3\stubs\debug\com\enestigli\dictionaryapp\data\locale\OwnDictionaryDatabase.java:7: warning: Schema export directory is not provided to the annotation processor so we cannot export the schema. You can either provide `room.schemaLocation` annotation processor argument OR set exportSchema to false.
public abstract class OwnDictionaryDatabase extends androidx.room.RoomDatabase {
FAILURE: Build failed with an exception.

* What went wrong:
Execution failed for task ':app:kaptDebugKotlin'.
&gt; A failure occurred while executing org.jetbrains.kotlin.gradle.internal.KaptWithoutKotlincTask$KaptExecutionWorkAction
   &gt; java.lang.reflect.InvocationTargetException (no error message)
Exception is:
org.gradle.api.tasks.TaskExecutionException: Execution failed for task ':app:kaptDebugKotlin'
Caused by: org.gradle.workers.internal.DefaultWorkerExecutor$WorkExecutionException: A failure occurred while executing org.jetbrains.kotlin.gradle.internal.KaptWithoutKotlincTask$KaptExecutionWorkAction
Caused by: java.lang.reflect.InvocationTargetException
at org.jetbrains.kotlin.gradle.internal.KaptExecution.run(KaptWithoutKotlincTask.kt:288)
    at org.jetbrains.kotlin.gradle.internal.KaptWithoutKotlincTask$KaptExecutionWorkAction.execute(KaptWithoutKotlincTask.kt:243)
Caused by: org.jetbrains.kotlin.kapt3.base.util.KaptBaseError: Error while annotation processing
    at org.jetbrains.kotlin.kapt3.base.AnnotationProcessingKt.doAnnotationProcessing(annotationProcessing.kt:130)
    at org.jetbrains.kotlin.kapt3.base.AnnotationProcessingKt.doAnnotationProcessing$default(annotationProcessing.kt:31)
    at org.jetbrains.kotlin.kapt3.base.Kapt.kapt(Kapt.kt:45)
Deprecated Gradle features were used in this build, making it incompatible with Gradle 8.0.

You can use '--warning-mode all' to show the individual deprecation warnings and determine if they come from your own scripts or plugins.
</code></pre>
<p><strong>OwnDicDao</strong></p>
<pre><code>@Dao
interface OwnDicDao {


    @Query(&quot;SELECT * FROM OwnDictionaries&quot;)
    suspend fun GetAllDictionary()

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun Insert(dictionary: OwnDicEntity)

    @Delete
    suspend fun Delete(dictionary: OwnDicEntity)

    @Query(&quot;DELETE FROM owndictionaries&quot;)
    suspend fun DeleteAll()

    @Query(&quot;UPDATE OwnDictionaries SET dicName =:dicName&quot;)
    suspend fun Update(dicId:Int?,dicName:String)



}
</code></pre>
<p>When I comment out the <code>@Query</code> anatations, that is, when I comment out the <code>Update</code> and <code>GetAllDictionary</code> functions, the problems disappear and the application works properly. I noticed this.</p>
<p><strong>for example like this</strong></p>
<pre><code>/*  @Query(&quot;UPDATE OwnDictionaries SET dicName =:dicName&quot;)
    suspend fun Update(dicId:Int?,dicName:String)*/

 /* @Query(&quot;SELECT * FROM OwnDictionaries&quot;)
    suspend fun GetAllDictionary()*/
</code></pre>
<p><strong>OwnDicEntity</strong></p>
<pre><code>@Entity(tableName = &quot;OwnDictionaries&quot;)
data class OwnDicEntity(

    @ColumnInfo(name = &quot;dicName&quot;) val ownDicName:String,
    @ColumnInfo(name = &quot;creationTime&quot;) val creationTime:String,
    @PrimaryKey(autoGenerate = true) val uid: Int? = null
)
</code></pre>
<p><strong>OwnDicDatabase</strong></p>
<pre><code>@Database(
    entities = [OwnDicEntity::class],
    version = 1
)

abstract class OwnDicDatabase: RoomDatabase() {

    abstract val ownDicDao: OwnDicDao
}
</code></pre>
<p><strong>build.gradle(Module)</strong></p>
<pre><code>plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
    id  'kotlin-kapt'
    id 'dagger.hilt.android.plugin'
    id 'org.jetbrains.kotlin.android.extensions'
}

android {
    compileSdk 32

    defaultConfig {
        applicationId &quot;com.enestigli.dictionaryapp&quot;
        minSdk 21
        targetSdk 32
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
        kotlinCompilerExtensionVersion compose_version
    }
    packagingOptions {
        resources {
            excludes += '/META-INF/{AL2.0,LGPL2.1}'
        }
    }
    androidExtensions {
        experimental = true
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.7.0'
    implementation &quot;androidx.compose.ui:ui:$compose_version&quot;
    implementation &quot;androidx.compose.material:material:$compose_version&quot;
    implementation &quot;androidx.compose.ui:ui-tooling-preview:$compose_version&quot;
    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.3.1'
    implementation 'androidx.activity:activity-compose:1.3.1'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.3'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.4.0'
    androidTestImplementation &quot;androidx.compose.ui:ui-test-junit4:$compose_version&quot;
    debugImplementation &quot;androidx.compose.ui:ui-tooling:$compose_version&quot;
    debugImplementation &quot;androidx.compose.ui:ui-test-manifest:$compose_version&quot;



    // Retrofit
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
    implementation &quot;com.squareup.okhttp3:okhttp:4.9.0&quot;
    implementation &quot;com.squareup.okhttp3:logging-interceptor:4.9.0&quot;

    //Dagger - Hilt
    implementation &quot;com.google.dagger:hilt-android:2.38.1&quot;
    kapt &quot;com.google.dagger:hilt-android-compiler:2.38.1&quot;
    //implementation &quot;androidx.hilt:hilt-lifecycle-viewmodel:1.0.0-alpha03&quot;
    kapt &quot;androidx.hilt:hilt-compiler:1.0.0&quot;
    implementation 'androidx.hilt:hilt-navigation-compose:1.0.0-alpha03'

    // Coroutines
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-core:1.5.1'
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.5.1'

    // Coroutine Lifecycle Scopes
    implementation &quot;androidx.lifecycle:lifecycle-viewmodel-ktx:2.3.1&quot;
    implementation &quot;androidx.lifecycle:lifecycle-runtime-ktx:2.3.1&quot;

    // Room
    implementation &quot;androidx.room:room-runtime:2.3.0&quot;
    kapt &quot;androidx.room:room-compiler:2.3.0&quot;


    // To use Kotlin annotation processing tool (kapt)


    // Kotlin Extensions and Coroutines support for Room
    implementation &quot;androidx.room:room-ktx:2.3.0&quot;


    //Material theme3
    implementation &quot;androidx.compose.material3:material3:1.0.0-alpha12&quot;
    implementation &quot;androidx.compose.material3:material3-window-size-class:1.0.0-alpha12&quot;

    //skrape{it}
    implementation 'org.jsoup:jsoup:1.12.1'

    //compose
    implementation &quot;androidx.compose.runtime:runtime-livedata:$compose_version&quot;


}
</code></pre>
<p><strong>build.gradle(Project)</strong></p>
<pre><code>// Top-level build file where you can add configuration options common to all sub-projects/modules.
buildscript {
    ext {
        compose_version = '1.0.1'
    }
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.2.2'
        classpath &quot;org.jetbrains.kotlin:kotlin-gradle-plugin:1.5.21&quot;
        classpath 'com.google.dagger:hilt-android-gradle-plugin:2.40.1'

        // NOTE: Do not place your application dependencies here; they belong
        // in the individual module build.gradle files
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
</code></pre>
<p>When I delete room completely, for example, when I delete classes such as dao, database, entity, it works as before, and as I said above, it works when I remove or comment @Query queries. What could be the problem, I've been dealing with these errors for 2 days. I have not encountered such errors when using room in my previous projects.</p>

## Answers
### Answer ID: 74303198
<p>The issue from as your quires returning some data so you need implement return type to suspend function like below</p>
<pre><code>    @Dao
interface OwnDicDao {


    @Query(&quot;SELECT * FROM OwnDictionaries&quot;)
    suspend fun GetAllDictionary():List&lt;OwnDicEntity&gt; // here change

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun Insert(dictionary: OwnDicEntity)

    @Delete
    suspend fun Delete(dictionary: OwnDicEntity)

    @Query(&quot;DELETE FROM owndictionaries&quot;)
    suspend fun DeleteAll() // here no change need because it returns nothing

    @Query(&quot;UPDATE OwnDictionaries SET dicName =:dicName&quot;)
    suspend fun Update(dicId:Int?,dicName:String):List&lt;OwnDicEntity&gt; //here change



}
</code></pre>

