from twilio.rest import Client

account_sid = 'AC115239e70f791cf8147ea00a3c0404f1'
auth_token = '012261aaacef9d2c97b953c25362a739'
client = Client(account_sid, auth_token)

call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+16692369058',
                        from_='+12056969542'
                    )

print(call.sid)

message = client.messages.create(
                              body='IMPORTANT REMINDER!\nYour reservation time is Up. Please remove your car.',
                              from_='+12056969542',
                              to='+16692369058'
                          )

print(message.sid)