

# Step2: Getting our app triggered when a user joins a channel and using the Web API

As a second step, we're going to modify our app so that it starts listening to the event generated when users join channels, and then we'll leverage the Web API to get the channel's topic and purpose, and send the joining user a message.



## Subscribing to additional events

- Go back to your app's config page (from https://api.slack.com/apps, click on your app's name)
- Click on "Event Subscriptions" (left column), and under "Subscribe to Bot Events", click on "add Bot User Event". Then, select `member_joined_channel` and hit "Save Changes" at the bottom of the page.
![subscribing to events](docs/step2-events.png)

Your app is now configured to receive payloads when a user joins a channel your bot user is a member of. Let's make sure our lambda function is able to handle them.


## Updating the function called by the EventsAPI lambda

- Open your EventsAPI Lambda function, and under Function code, you'll see a "Handler" box. This is where we tell Lambda which python function should be ran when a request is received. The CloudFormation template we ran uploaded the code and dependencies for the 3 different steps, so we'll only need to point the handler to the right function: replace `event_step1.event_handler` with `event_step2.event_handler`, and hit save.
![Lambda handler](docs/step2-Lambda_handler.png)





## Getting a welcome message

- Invite your bot to a channel: you will only receive events if your bot is a member of the channel
- Set a purpose / topic
- Leave and rejoin to trigger the `member_joined_channel` event, or invite a new user to the channel
- The joining user will receive an ephemeral message from the bot.

## How does this work

- When a user joins a channel that our bot is a member of, Slack Events API will send a `member_joined_channel` event to our `/events` endpoint
- The request will be passed to the Lambda function, which will call the `conversations.info` endpoint of the Web API, and extract the channel's topic and purpose .
- Then, the Lambda will call the `chat.postEphemeral` endpoint in order to send a message to the joining user.

Hint: A good way to understand more about the app's logic and its corresponding code is to compare the `event_step1.py` and `event_step2.py` files. 

![architecture diagram](docs/step2-diagram.png)