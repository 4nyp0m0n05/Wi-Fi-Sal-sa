package edu.sakarya.testinet.network;

public interface TaskFinished<T> {
    void onTaskFinished(T data);
}
