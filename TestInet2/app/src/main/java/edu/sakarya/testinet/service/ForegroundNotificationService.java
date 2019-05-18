package edu.sakarya.testinet.service;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.graphics.Color;
import android.os.Build;
import android.os.IBinder;
import android.support.annotation.Nullable;
import android.support.v4.app.NotificationCompat;
import edu.sakarya.testinet.MainActivity;
import edu.sakarya.testinet.R;
import edu.sakarya.testinet.network.InternetAvailabilityChecker;
import edu.sakarya.testinet.network.InternetConnectivityListener;

import static edu.sakarya.testinet.MyApp.CHANNEL_ID;

public class ForegroundNotificationService extends Service implements InternetConnectivityListener {

    private NotificationManager notificationManager;
    private InternetAvailabilityChecker mInternetAvailabilityChecker;

    @Override
    public void onCreate() {
        super.onCreate();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            notificationManager = getSystemService(NotificationManager.class);
        }
        mInternetAvailabilityChecker = InternetAvailabilityChecker.getInstance();
        mInternetAvailabilityChecker.addInternetConnectivityListener(this);
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        String input;
        int icon;
        Boolean isConnect = intent.getBooleanExtra("isConnect", false);
        int color;
        if (isConnect) {
            input = "Connect";
            color = R.color.colorPrimary;
            icon = R.drawable.ic_check_circle;
        } else {
            input = "Not Connect";
            color = R.color.colorAccent;
            icon = R.drawable.ic_warning;
        }

        Intent notificationIntent = new Intent(this, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, notificationIntent, 0);


        Notification notification = new NotificationCompat.Builder(this, CHANNEL_ID)
                .setSmallIcon(icon)
                .setContentText(input)
                .setContentTitle("Connect Status")
                .setContentIntent(pendingIntent)
                .setColor(color)
                .build();

        startForeground(2, notification);

        return START_NOT_STICKY;
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onInternetConnectivityChanged(boolean isConnected) {
        if (isConnected) {
            NotificationCompat.Builder notification = new NotificationCompat.Builder(this, CHANNEL_ID)
                    .setSmallIcon(R.drawable.ic_check_circle)
                    .setContentText("Connect")
                    .setColor(Color.GREEN)
                    .setContentTitle("Connection Status");

            notificationManager.notify(2, notification.build());
        } else {
            NotificationCompat.Builder notification = new NotificationCompat.Builder(this, CHANNEL_ID)
                    .setSmallIcon(R.drawable.ic_warning)
                    .setContentText("Not Connect")
                    .setColor(Color.YELLOW)
                    .setContentTitle("Connection Status");

            notificationManager.notify(2, notification.build());
        }
    }

    @Override
    public void onDestroy() {
        mInternetAvailabilityChecker.removeInternetConnectivityChangeListener(this);
    }
}
