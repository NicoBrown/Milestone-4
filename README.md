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

------

## Testing

------

## Deployment

------

## Credits

------

### Code



### Media

