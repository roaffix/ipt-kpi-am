import com.hazelcast.core.*;
import com.hazelcast.config.*;

public class GettingStarted {
    public static void main(String[] args) {
        XmlConfigBuilder configBuilder = new XmlConfigBuilder();
        Config config = configBuilder.build();

        HazelcastInstance hazelcastInstance = Hazelcast.newHazelcastInstance(config);
        hazelcastInstance.getPartitionService().addPartitionLostListener( new ConsoleLoggingPartitionLostListener() );

        IMap<Integer, String> capitals = hazelcastInstance.getMap("capitals");

        System.out.println("Get 3 capital: " + capitals.get(3));
        System.out.println("Map Size:" + capitals.size());

    }
}
