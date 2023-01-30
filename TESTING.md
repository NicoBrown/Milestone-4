<div align="center">
  
# TESTING
</div>

During the development of the application variables were written to the console as the project was built, the django debug tools were also invaluable to highlight errors and enable variables to be read. 

Initial models were developed for the users, profile and expenses using Figma:

![image](https://user-images.githubusercontent.com/69271605/215613452-c3cc756e-d520-4826-b498-4ee2335f67f6.png)

As the project developed the required fields for each of the models were expanded to cover more functionality. Users were required to onboard with stripe and verify their details before creating expenses and accepting payouts from the platform, this resulted in a number of changes to the UserProfile model

![image](https://user-images.githubusercontent.com/69271605/215607181-5a3850ab-c6f8-4f33-9aa9-596312ad22a8.png) ![image](https://user-images.githubusercontent.com/69271605/215607235-29c00443-0970-46cc-88a5-4fc25a9e4d5a.png) ![image](https://user-images.githubusercontent.com/69271605/215607451-a1fd4afc-8ebe-4118-b477-cce1d142f99c.png)

### User Testing

I tested the user workflows by performing the actions outlined in the user stories, the basic methodology was:

  1. I signed up the platofrm and performed the required email verification
  2. On-boarded with Stripe by clicking the banner on the user-home page, and was returned to the same page when complete
  3. if I on-boarded correctly and no other requirements were due, the banner would disapear
  4. I Followed the link to add other test users to enable me to split bills, I entered their name in the search field and followed them
  5. I could then click to add an expense from user-home page
  6. I can then upload a reciept image
  7. I Edit the returned google cloud processed expense if needed and divided it between the users and noted the user name down
  8. I then checked the expense was visible on the users home page
  9. Using the profile that was assinged the expense I performed steps 1-3 above
  10. I could then check out using the expense created earlier
  11. Perform the checkout flow with stripe
  12. Receive on-screen confirmation of the expense being paid
  13. The expense would move from unpaid to the paid tab

### Lighthouse

I used lighthouse to identify issues with page loading and rendering blockers. in the first instance the page loading time and first contentful paint was for too slow and resulted in a performance score of 64 and nearly 7 seconds until the page had rendered:

![image](https://user-images.githubusercontent.com/69271605/215600920-d0a7a5fd-7a4f-418b-abe8-f5f2ce5c8f31.png)

I optimised the time by removing some redundant libraries from the base.html file, pre-loading the MDN css file and using a minified version, adding lazy loading to images which couldnt be seen when you naviagted to the home page. This resulted in the loading time being more than halved:

![image](https://user-images.githubusercontent.com/69271605/215601892-b7389bbc-1a7b-40ce-bfdd-47e697836696.png)

### HTML validation

I used the HTML validator at https://validator.w3.org/ to test the website, a number of issues were identified by the validator and fixed.

### Google Cloud AI

I used the [demo](https://cloud.google.com/document-ai#section-2) on the google developer website to check the processing output for a number of receipts. I decided on using the expenses Processor based on this. I created an implementation using the python Client Library and printed the result to the console where I imported it into [JSON crack](https://jsoncrack.com/), the image below is taken from the canvas in which the response was visulised. This enabled me to see the response more clearly and implement a method to process the genral and line item data to display it in a template for the user to edit.

![image](https://user-images.githubusercontent.com/69271605/215599511-0661b2e6-8280-4bbc-9890-8a8211f6333f.png)

Mock data should be created for the API in future to reduce the number of API calls as there was a significant expense incurred while testing and development.

### Stripe Connect

Each user is on-boarded to the Connect platform as a [custom](https://stripe.com/docs/connect/custom-accounts) user with stripe handling the on-boarding and verification process and then directing the users back to the web app. Stripe is currently set to developer mode on the platforms dashboard so that the documents required to verify identity can be easily accessed and checkout flows do not debit accounts if used, there is also a monthly associated cost for having active users registered as connect accounts which is being avoided.

### Bugs encountered at deployment

- Google Cloud was returning a 500 response due to the credentials not being read from the Heroku environment variables until the related buildpack was added
- Stripe was unable to return users to the webiste after onboarding and payments due to incorrect hardcoded URL's

### Issues for future development

- More logic should be present in the models rather than the views, the templates are also logic heavy in some cases containing javascript elements to update input values
- The ability to split tips has not been implemented so far, a model method could be added to the orderline item to query the number of line items in the expense, divide the tip up and add that to the line items total before it is saved
- Amazon S3 set to public so documents can be seen by the public and is not secure
- A personal email was used for the google SMPT
- The onboarding with stripe could be performed in one step and more information could be shared between the platform and stripe.
- The validation on expense form is lacking - this should be handled by a formset containing an expense form and a number of orderline items forms created dynamically using an inline formset or formsetfactory method before the template is rendered inside of the expense views.py file
