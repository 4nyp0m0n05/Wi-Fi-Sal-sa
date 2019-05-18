package edu.sakarya.testinet;

import android.app.Application;
import android.app.NotificationChannel;
import android.app.NotificationManager;

import edu.sakarya.testinet.network.InternetAvailabilityChecker;

public class MyApp extends Application {

    public static final String CHANNEL_ID = "channel_ssl_notification";
    public static final String WifiCHANNEL_ID = "wifi_Receiver_Channel_ID";

    @Override
    public void onCreate() {
        super.onCreate();
        InternetAvailabilityChecker.init(this);

        createNotificationChannel();

    }

    private void createNotificationChannel() {

        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(CHANNEL_ID,
                    "NotificationChannel SSL",
                    NotificationManager.IMPORTANCE_DEFAULT);
            NotificationChannel channel2 = new NotificationChannel(WifiCHANNEL_ID,
                    "Wifi Channel ID",
                    NotificationManager.IMPORTANCE_DEFAULT);

            NotificationManager manager = getSystemService(NotificationManager.class);
            manager.createNotificationChannel(channel);
            manager.createNotificationChannel(channel2);
        }

    }

    @Override
    public void onLowMemory() {
        super.onLowMemory();
        InternetAvailabilityChecker.getInstance().removeAllInternetConnectivityChangeListeners();
    }

}
