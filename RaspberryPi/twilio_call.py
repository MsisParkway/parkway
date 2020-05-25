from twilio.rest import Client

account_sid = 'TEST'
auth_token = 'TEST'
client = Client(account_sid, auth_token)

call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+14086462243',
                        from_='+12058581270'
                    )

print(call.sid)

message = client.messages.create(
                              body='IMPORTANT REMINDER!\nYour reservation time is Up. Please remove your car.',
                              from_='+12058581270',
                              to='+14086462243'
                          )

print(message.sid)