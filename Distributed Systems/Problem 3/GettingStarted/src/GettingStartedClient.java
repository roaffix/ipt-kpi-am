/*package com.hazelcast.test;

import com.hazelcast.client.config.ClientConfig;
import com.hazelcast.client.HazelcastClient;
import com.hazelcast.core.HazelcastInstance;
import com.hazelcast.core.IMap;
import com.hazelcast.config.*;

public class GettingStartedClient {
    public static void main(String[] args) {
        ClientConfig clientConfig = new ClientConfig();
        //clientConfig.addAddress("10.17.29.15:5701");
        HazelcastInstance client = HazelcastClient.newHazelcastClient(clientConfig); //create hazelcast client

        IMap map = client.getMap("capitals"); // access to distributed map

        System.out.println("Get 2 capital: " + map.get("2"));
        System.out.println("Map Size:" + map.size());
    }
}*/