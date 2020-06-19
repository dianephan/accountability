import com.twilio.Twilio;
import com.twilio.rest.api.v2010.account.Message;
import com.twilio.type.PhoneNumber;
import com.twilio.Twilio;


public class SmsSender {
    public static final String ACCOUNT_SID = System.getenv("TWILIO_ACCOUNT_SID");
    public static final String AUTH_TOKEN = System.getenv("TWILIO_AUTH_TOKEN");

    public static void main(String[] args) {
        Twilio.init(ACCOUNT_SID, AUTH_TOKEN);

        Message message = Message
                .creator(new PhoneNumber("+14086434472"), // to
                        new PhoneNumber("+19145296977"), // from
                        "Where's Wallace?")
                .create();

        System.out.println(message.getSid());
    }
}

// throw the downloaded jar file into the same 
// javac -cp twilio-7.52.0-jar-with-dependencies.jar SmsSender.java
// java -cp .:twilio-7.52.0-jar-with-dependencies.jar SmsSender
// Secure your environment var https://www.twilio.com/docs/usage/secure-credentials
