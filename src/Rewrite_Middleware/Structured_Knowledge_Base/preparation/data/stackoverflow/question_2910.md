# Angular custom validation with async service
[Link to question](https://stackoverflow.com/questions/58221050/angular-custom-validation-with-async-service)
**Creation Date:** 1570112079
**Score:** 0
**Tags:** javascript, angular, firebase, google-cloud-firestore, angularfire2
## Question Body
<p>I am using Angular with a Firestore database (with Angularfire2). To check wheter a username already exists, I made a custom validation class with a validate function. Unfortunately, no matter if the validate function returns null or { emailTaken: true }, the form seems to stay invalid. If I rewrite the function to only return null it works, so I suppose the error is located in this function - maybe it has something to do with it being async?</p>

<p>NameValidator class: </p>

<pre><code>import { FirebaseService } from './../services/firebase.service';
import { FormControl } from "@angular/forms";
import { Injectable } from '@angular/core';

@Injectable()
export class NameValidator {
  constructor(private firebaseService: FirebaseService) { }

  validate(control: FormControl): any {
    return this.firebaseService.queryByUniqueNameOnce(control.value).subscribe(res =&gt; {
        return res.length == 0 ? null : { emailTaken: true };
    });
  }
}
</code></pre>

<p>The firebaseService query function:</p>

<pre><code>queryByUniqueNameOnce(uniqueName: string) {
 return this.firestore.collection("users", ref =&gt; ref.where('uniqueName', '==', uniqueName))
 .valueChanges().pipe(take(1));
}
</code></pre>

<p>The formGroup:</p>

<pre><code> this.firstForm = this.fb.group({
  'uniqueName': ['', Validators.compose([Validators.required, this.nameValidator.validate.bind(this.nameValidator)])],
});
</code></pre>

## Answers
### Answer ID: 58221122
<p>Async validators are to be the third parameters of the form control. </p>

<p>Also, <code>compose</code> is rendered useless in the newest versions. </p>

<pre><code>'uniqueName': ['', [/*sync validators*/], [this.nameValidator.validate]]
</code></pre>

<p>You also will have to change your validation function : </p>

<pre><code>  validate(control: FormControl): any {
    return this.firebaseService.queryByUniqueNameOnce(control.value).pipe(
      map(res =&gt; !res.length ? null : ({ emailTaken: true }) )
    );
  }
</code></pre>

