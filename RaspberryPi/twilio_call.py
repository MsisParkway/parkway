from twilio.rest import Client

account_sid = 'AC366a7dce13a2f2f0f18fc6727ba88ace'
auth_token = 'bc8e109e23d25deb7e32dc6c2a2187e0'
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