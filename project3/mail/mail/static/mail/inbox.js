document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', (event) => {
    send_email();
    event.preventDefault();
  });
  document.querySelector('#email-view');

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
};


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  document.querySelector('#emails-view-title').innerHTML = 
    `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  document.querySelector('#emails-view-table').innerHTML = null;
  
  // Get emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      
    // Show emails 
    emails.forEach(email => {
      
      let email_id = `email-${email.id}`;
      let email_item = document.querySelector(`#${email_id}`);
      
      // create parent div and set properties
      email_item = document.createElement('div');
      email_item.id = `email-${email.id}`;
      email_item.classList.add('row', 'border');
      document.querySelector('#emails-view-table').appendChild(email_item); 
      if (email.read === true) {
        email_item.style.backgroundColor = 'WhiteSmoke';
      };

      // create content div and set properties
      email_contents = document.createElement('div');
      email_contents.id = `email-${email.id}-content`;
      email_contents.classList.add("col");
      email_contents.addEventListener('click', () => show_email(email));
      email_fields(email, ['sender', 'subject', 'timestamp'], email_contents);  
      email_item.appendChild(email_contents);   

      // create button div
      email_buttons = document.createElement('div');
      email_buttons.id = `email-${email.id}-buttons`;
      email_buttons.classList.add("col-2");
      email_item.appendChild(email_buttons);   

      // create archive button
      if (mailbox === 'inbox') {
        create_archive_button(email, true, email_buttons, 'Archive');
      };
    });
  });
};


 // send email
 function send_email() {

  // get form input
  recipients = document.querySelector('#compose-recipients').value;
  subject = document.querySelector('#compose-subject').value;
  body = document.querySelector('#compose-body').value;

 // send email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  // without timeout, load_mailbox occurs before PUT request 50% of the time
  }).then(setTimeout( () => {load_mailbox('sent')},20)); 
};


// Show email
function show_email(email) {
  let email_view_element = document.querySelector('#email-view');
  email_view_element.innerHTML = null;

  // Show email view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  email_view_element.style.display = 'block';
  
  // Retreive email data
  fetch(`/emails/${email.id}`)
  .then(response => response.json())
  .then(email => email_fields(email, ['sender','recipients', 'subject', 'timestamp', 'body'], email_view_element));

  // Mark email as read
  fetch(`/emails/${email.id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true
    })
  });

  // Unarchive button
  if (email.archived === true) {
    create_archive_button(email, false, email_view_element, 'Unarchive');
  };

  // Reply button
  create_reply_button(email, email_view_element);
};


// create button to reply
function create_reply_button(email, parent) {
  
  // create button and set properties
  button = document.createElement('button');
  button.id = `email-${email.id}-archive`;
  button.classList.add('btn', 'btn-primary', 'btn-block', 'py-4');
  parent.appendChild(button);   
  button.innerHTML = 'Reply';

  // got to compose-view and prefill fields
  button.addEventListener('click', () => {
    compose_email();
    document.querySelector('#compose-recipients').value = email.sender;
    if (email.subject.slice(0,4) != 'Re: ') {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    } else {
      document.querySelector('#compose-subject').value = email.subject;
    };
    document.querySelector('#compose-body').value = 
      `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
  });
};


// create button for archiving or unarchiving
function create_archive_button(email, target_state, parent, text) {
 
  // create button and set properties
  button = document.createElement('button');
  button.id = `email-${email.id}-archive`;
  button.classList.add('btn', 'btn-primary', 'btn-block', 'py-4');
  parent.appendChild(button);   
  button.innerHTML = text;

  // update archived state
  button.addEventListener('click', () => {
    fetch(`/emails/${email.id}`, {
      method: "PUT",
      body: JSON.stringify({
      archived: target_state
      })
    // without timeout, load_mailbox occurs before PUT request 50% of the time
    }).then(setTimeout( () => {load_mailbox('inbox')},20));
  });
};


// take an email, list of fields and parent element
// create elements containing the fields and append to parent
function email_fields(email, fields, parent) {
  for (const field of fields) {
    if (field in email) {    
      const field_id = `email-${email.id}-${field}`;

      // checking if field element already exists
      let field_element = parent.querySelector(`#${field_id}`);
      if (!field_element) {
        field_element = document.createElement('div');
        field_element.id = field_id;
        if (field === 'body') {
          field_element.classList.add('body', 'border-top');

        };
        field_element.innerHTML = `${field}: ${email[field]}`;
        console.log(email[field]);
        parent.appendChild(field_element); 
      };
    };
  };
};