// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';
 
const functions = require('firebase-functions');
const {WebhookClient} = require('dialogflow-fulfillment');
const {Card, Payload, Suggestion} = require('dialogflow-fulfillment');
const crypto = require('crypto');

// Node Mailer Declaration
const nodemailer = require('nodemailer');
const transporter = nodemailer.createTransport({
  service: 'gmail',
      auth: {
        user: "GCP_ACC_EMAIL",
        pass: "GCP_APP_KEY"
      }
});

//Firebase Declaration
const admin = require('firebase-admin');
const serviceAccount = SERVICEACCOUNTKEYHERE; //GET SERVICE ACCOUNT KEY FROM GCP
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "DBURLHERE" //FIREBASE DB URL
});

process.env.DEBUG = 'dialogflow:debug';
 
exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));
 
  function sendStudentEnquiry(agent){
    const email = agent.parameters.email;
    const name = agent.parameters.name;
    const message = agent.parameters.message;
    
    const mailOptions = {
      from: 'GCP_ACC_EMAIL',
      to: 'TUTOREMAILHERE', //TUTOR'S EMAIL
      subject: "Student's Enquiry from Chatbot",
      text: "Hi, \n\n A student has questions on the subject. Please review." + 
      '\n\n Student: ' + name + '\n\n Email: ' + email + '\n\n Enquiry: ' + message + 
      '\n\n Best Regards, \n Dialogflow Chatbot'
    };
    
    transporter.sendMail(mailOptions, function(error, info){
      if (error) {
        agent.add("Error while sending");
        console.log(error);
      } 
      
      else {
        agent.add("📧 Email sent!");
        console.log('Email sent: ' + info.response);
      }
    });
  }
  
  function loginGreeting(agent)
  {
    const hash = crypto.createHash('sha224');
    const string = agent.parameters.loginID;
    const hashedString = hash.update(string, 'utf-8');
    const gen_hash = hashedString.digest('hex');

    var id;
    var ref = admin.database().ref("ID");
    ref.orderByValue().equalTo(gen_hash).on("child_added", function(snapshot){
      id = snapshot.key;
    });

    return admin.database().ref().once("value").then(function(snapshot) {
      var name = snapshot.child("/NAME/"+id).val();
      agent.add("Login Successful! 💁🏻‍♀️");
      agent.add("Hi "+ name + ", how do you feel today? 🧐");
      const payload = {
                        "richContent": [
                          [
                            {
                              "type": "chips",
                              "options": [
                                {
                                  "text": "Awesome 😄"
                                },
                                {
                                  "text": "Doing fine 🙂"
                                },
                                {
                                  "text": "Still hanging there 😐"
                                },
                                {
                                  "text": "It's been a rough week 😔"
                                }
                              ]
                            }
                          ]
                        ]
                      };
      agent.add(new Payload(agent.UNSPECIFIED, payload, { rawPayload: true, sendAsMessage: true }));
      //agent.add(new Payload(agent.TELEGRAM, payloadTele, {rawPayload: true, sendAsMessage: true}));

    });
  }

  function remembername(agent)
  {
    const hash = crypto.createHash('sha224');
    const string = agent.parameters.loginID;
    const hashedString = hash.update(string, 'utf-8');
    const gen_hash = hashedString.digest('hex');

    var id;
    var ref = admin.database().ref("ID");
    ref.orderByValue().equalTo(gen_hash).on("child_added", function(snapshot){
      id = snapshot.key;
    });

    return admin.database().ref().once("value").then(function(snapshot) {
      var name = snapshot.child("/NAME/"+id).val();
      agent.add("Hi "+ name + ", welcome back!");
      const payload = {
                        "richContent": [
                          [
                            {
                              "type": "chips",
                              "options": [
                                {
                                  "text": "Learn & Explore"
                                }
                              ]
                            }
                          ]
                        ]
                      };
      const payloadTele = {

        "telegram": {

          "text": "Select a menu:",

          "reply_markup": {

              "keyboard": [

                [

                    {

                    "text": "🔎 Learn & Explore",

                    "callback_data": "Learn & Explore"

                    }

                ],
              ]

          }

        }

      };
      agent.add(new Payload(agent.UNSPECIFIED, payload, { rawPayload: true, sendAsMessage: true }));
      agent.add(new Payload(agent.TELEGRAM, payloadTele, { rawPayload: true, sendAsMessage: true }));

    });
  }

  function captureSocialTag(agent){
	  console.log('Telegram Payload: ' + request.body.originalDetectIntentRequest.payload);
    console.log('Telegram Social Tagging Participated Username: ' + request.body.originalDetectIntentRequest.payload.data.from.username);
    agent.add("🥰 Thank you for answering your classmate's query!");
    agent.add("💁 To continue browsing, please select the menu commmand by typing '/'.");
  }


  // Run the proper function handler based on the matched Dialogflow intent name
  let intentMap = new Map();
  intentMap.set('Email Enquiry', sendStudentEnquiry);
  intentMap.set('Login', loginGreeting);
  intentMap.set('Login - Remember Name', remembername);
  intentMap.set('Login - Fallback - yes - fallback', captureSocialTag);
  agent.handleRequest(intentMap);
});
