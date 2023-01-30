<h1 align="center" >QuikSplit</h1>

<h3 align="center" >Quickly split bills with anyone just by taking a photo of the receipt!</h3>

<br> 

[View the live project here](https://kwik-split.herokuapp.com/)

### Table of Contents
**[Introduction](#introduction)**<br>
**[Technologies used](#technologies-used)**<br>
**[Design](#design)**<br>
**[User Experience (UX)](#user-experience-ux)**<br>
**[Testing](#testing)**<br>
**[Deployment](#deployment)**<br>
**[Credits](#credits)**<br>

## Introduction

This project is for the milestone project 4 of the Code Institutes Full Stack Developer Course, this Application will allow a user to take a photo of a recipt or invoice and split the costs with other users. A good example of where this would be useful is for dinner out with friends, or for on-going expenses while on a group holiday, or even for work expenses.

A recipt is processed using google clouds Document AI and then the resulting line items can be assigned to different users. The user can create, read, update and delete the expense records and their profile information. Users payouts are processed by stripe using the connect service. Each account is onboarded, where their bank account and identification information is confirmed to reduce financial loss and increase security. 

## Technologies used
  #### Front End
    - Material Design for Bootstrap (MDB)
    - HTML
    - Fontawesome icons
    - In product help/guide - Tourguide.js
    - Custom CSS
    - Django Templating
  #### Back End  
    - Django
    - Python
    - AWS S3 storage
    - Heroku
    - Elephant SQL
    - Google Cloud Document AI

## Design

The initial site design was mocked up in Miro across three different screen sizes; mobile, tablet and desktop. The site was designed as mobile first and responsive and scaled to other screen sizes where needed usign media queries and by un-stacking columns above the XL breakpoint. 

The breakpoint were set to the 6 default MDB breakpoints:

<table class="table table-striped">
      <thead>
        <tr>
          <th>Breakpoint</th>
          <th>Class infix</th>
          <th>Dimensions</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>X-Small</td>
          <td><em>None</em></td>
          <td>0–576px</td>
        </tr>
        <tr>
          <td>Small</td>
          <td><code>sm</code></td>
          <td>≥576px</td>
        </tr>
        <tr>
          <td>Medium</td>
          <td><code>md</code></td>
          <td>≥768px</td>
        </tr>
        <tr>
          <td>Large</td>
          <td><code>lg</code></td>
          <td>≥992px</td>
        </tr>
        <tr>
          <td>Extra large</td>
          <td><code>xl</code></td>
          <td>≥1200px</td>
        </tr>
        <tr>
          <td>Extra extra large</td>
          <td><code>xxl</code></td>
          <td>≥1400px</td>
        </tr>
      </tbody>
    </table>

------

## User experience (UX)

The site was designed with a responsive top navigation bar which displayed the log in/out buttons and links to the home page and the users home page.

### User Stories

The site was designed as a web app in which the user can easily split a bill with another user. Some high-level user stories were developed at the start of the project to define which features to implement:

- as a user, I want to be able to search for and follow other users, so I can split a bill with them.
- as a user, I want to be able to update my profile information.
- as a user, I want to be able to calculate a bill amount, so that I can request payment.
- as a user, I want to be able to easily split a bill with other users.

The app was developed with these in mind along with some technical requirements for the application, onboarding and payment flows to be secure.

### Initial Wire-frames

I created a number of wire-frames as a part of the project development to inform the design as I worked, these were updated as the project progressed and I had more familiarity with the CSS/component library in use, MDB.
The wire-frames were shown as mobile first and expanded on for larger screen sizes where component layouts would be changed.

### Product Tour

I provided an interactive tour on the users homepage and the page in which you define an expense. The tour is intiated by a floating button on the page which then explains the features of the page and how to use the app.

The library used was tourguide.js, it was set up by adding data attributes to the html elements which defined the position in the product tour and the title and message for each of the elements covered in the tour.

------

## Testing

Testing is a manual process in which I performed functional and user acceptance testing on the application. I used in-browser testing tools to check for the functional requirements such as adequate loading times, accessability, etc. I then performed User acceptance testing by manually testing each flow in the app to ensure that it works as expected from a users perspective the deliver the user stories. I have further documented the testing work undertaken in the TESTING.md file located in this repository.

Below, I have outlined the identification and bank account details needed in order to test the third party stripe onboarding and payment flows in which the user is taken away from the app domain to stripe and then returned once completed either successfully or unsuccessfully.

### Stripe Connect

Stripe connect is currently in developer/testing mode so that user information doesnt have to be handled and verified. When a user in onboarded, they are redirected to a URL generated by stripe which then guides them through the onboarding process. A user has to confirm their phone number to receive a verification code, their identity and bank account for payouts. For testing, different information can be input to generate dofferent HTTP responses, the input data will be defined below:

#### Test dates of birth
Use these dates of birth (DOB) to trigger certain verification conditions.

<table><thead><tr><th style="width: 200px;">DOB</th><th style="width: 900px;">Type</th></tr></thead><tbody><tr><td><code>1901-01-01</code></td><td>Successful verification. Any other DOB results in unsuccessful verification.</td></tr><tr><td><code>1902-01-01</code></td><td>Successful, immediate verification. The verification result is returned directly in the response, not as part of a <span><span><a title="webhook" class="UnstyledLink InlineLink Text-color--blue Glossary-term no-api-tag" href="/docs/webhooks">webhook</a></span></span> event.</td></tr><tr><td><code >1900-01-01</code></td><td>This DOB triggers an Office of Foreign Assets Control (OFAC) alert.</td></tr></tbody></table>

#### Trigger bank account ownership verification

<div class="Table Table--striped Box-root Padding-vertical--12" style="position:relative"><table><thead><tr><th style="width: 118px;">Routing</th><th style="width: 141px;">Account</th><th style="width: 569px;">Type</th></tr></thead><tbody><tr><td><code class="InlineCode">110000000</code></td><td><code class="InlineCode">000999999991</code></td><td>Triggers the bank account ownership verification process after a short delay</td></tr></tbody></table></div>

#### Simulate requirements
If your platform has connected accounts in different countries or plans to, you might need to verify a person’s address as well as their identity (depending on the country). Stripe provides a sample date of birth (DOB) and sample addresses to test for this requirement.

<div class="Table Table--striped Box-root Padding-vertical--12" style="position:relative"><table><thead><tr><th style="width: 260px;">Information provided</th><th style="width: 186px;">Person verification status</th><th style="width: 382px;">requirements[currently_due]</th></tr></thead><tbody><tr><td>Verified date of birth and verified address</td><td>Verified</td><td>None</td></tr><tr><td>Verified date of birth and unverified address</td><td>Unverified</td><td><code class="InlineCode">verification.additional_document</code></td></tr><tr><td>Unverified date of birth and verified address</td><td>Unverified</td><td><code class="InlineCode">verification.document</code></td></tr><tr><td>Unverified date of birth and unverified address</td><td>Unverified</td><td><code class="InlineCode">verification.additional_document</code>, <code class="InlineCode">verification.document</code></td></tr></tbody></table></div>

The app is currently set to development model in stripe so that users can onboard without having to provide sensitive documents and bank account information. The stripe onboarding screen indicates its in test mode and you can click to use the test documents they provide.

------

## Deployment

The application is uses a number of third party services, libraries and API's which need to be set up individually in order to deploy the application. To get started clone a copy of this repo, if you do not know how to do this refer to this [git-guide](https://github.com/git-guides/git-clone). Once you have the project open in your IDE, run the command 
`pip install -r requirements.txt` in the terminal to install the required packages.

To configure the project to run you'll need to change the django settings and some environment variables. Ive used the python dotenv library to assist with this locally, an example .env file is shown below, this should be placed in the root of your project:

### Django

There are a few different variables which can be set to have the project run locally or when deployed. if USE_AWS is set then the projects media and static files will refer to the files available on AWS, these can be updated by running `python3 manage.py collectstatic` to push your files to the platform.
if DEVELOPMENT is set then django will report verbose errors to the user, which is useful for development but should be unset in deployment. New users are required to confirm their email addresses by opening a link emailed to them, with DEVELOPMENT set the email will be displayed on the console as a SMPT mail server wont work until its deployed.



### Python

### AWS S3 storage

### Heroku

### Elephant SQL

### Google Cloud Document AI

### Google email
------

## Credits

------

### Code
The project used the code institutes template for Gitpod as a starting point and took a lot of boiler plate code from the Boutique Ado project.

There were a number of tutorials I followed and took inspiration from in the development of the project:

- Django Social network app - https://testdriven.io/blog/setting-up-stripe-connect-with-django/

- Peer to Peer payment app - https://www.twilio.com/blog/create-peer-to-peer-payment-app-laravel-stripe


### Media

