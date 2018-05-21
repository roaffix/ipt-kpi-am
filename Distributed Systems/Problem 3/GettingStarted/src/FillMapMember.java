import com.hazelcast.core.*;

import java.util.Map;

public class FillMapMember {
    public static void main(String[] args) {
        HazelcastInstance hazelcastInstance = Hazelcast.newHazelcastInstance();
        Map<String, String> customers = hazelcastInstance.getReplicatedMap( "customers" );

        customers.put( "1", "Alex" );
        customers.put( "2", "Anton" );
        customers.put( "3", "Kate" );

        System.out.println("Map Size:" + customers.size());
    }
}