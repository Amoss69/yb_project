import { useNavigation } from "@react-navigation/native";
import React, { useContext, useEffect, useRef, useState } from "react";
import { Button, StyleSheet, View, BackHandler, Text } from "react-native";
import MapView, { Marker } from "react-native-maps";
import { MarkerContext, UserContext } from "../context/AppContext";

export default function MapScreen() {
  const navigation = useNavigation();
  const user = useContext(UserContext);
  const markerContext = useContext(MarkerContext);
  const [markers, setMarkers] = useState([]);
  const [selectedMarker, setSelectedMarker] = useState<string | null>(null);
  const requestedMarkers = useRef(false);

  if (!user) return null;
  const { webSocket, userId } = user;

  useEffect(() => {
    webSocket.setOnMessage((msg) => GetMarkers(msg, setMarkers));

    if (!requestedMarkers.current) {
      requestedMarkers.current = true;
      webSocket.sendData(`marker|get_markers|${userId}`);
    }

    return () => webSocket.setOnMessage(null);
  }, []);

  return (
    <View style={{ width: "100%", height: "100%" }}>
      <MapView
        style={styles.map}
        initialRegion={{
          latitude: 31.7683,
          longitude: 35.2137,
          latitudeDelta: 0.05,
          longitudeDelta: 0.05,
        }}
        onPress={(event) => {
          const { latitude, longitude } = event.nativeEvent.coordinate;
          markerContext?.setMark_latitude(latitude);
          markerContext?.setMark_longitude(longitude);
        }}
      >
        {markers.map((marker, index) => (
          <Marker
            key={index}
            coordinate={{ latitude: marker.latitude, longitude: marker.longitude }}
            image={markerImages[marker.type.toLowerCase()]}
            title={marker.type}
            onPress={() => {setSelectedMarker(marker.id)}
          }
          />
        ))}

        {markerContext?.Mark_latitude != null && markerContext?.Mark_longitude != null && (
          <Marker
            coordinate={{ latitude: markerContext.Mark_latitude, longitude: markerContext.Mark_longitude }}
            title="Selected Location"
          />
        )}
      </MapView>

      <View style={{ position: "absolute", bottom: 70, right: 15, padding: 5, borderRadius: 5}}>
        {markerContext?.Mark_latitude == null && markerContext?.Mark_longitude == null ? null : (
          <Button title="Choose Mark" color = "green" onPress={() => navigation.navigate("MarkerSelect")} />
        )}
      </View>


      <View style={{ position: "absolute", bottom: 68, left: 10 , padding: 5, borderRadius: 5}}>
        {selectedMarker != null && (
        <Button
        title="Remove Mark"
        color="red"
        onPress={() => {
        webSocket.sendData(`marker|remove|${selectedMarker}`); //sends the id of the marker to be removed to the server
        setSelectedMarker(null);
        }}/>
        )}
      </View>

      <View style={{ position: "absolute", bottom:35, left: 15}}>
        <Button
          title = "go back"
          onPress={() => {webSocket.sendData('user_go_login'); requestedMarkers.current = false; navigation.navigate("Login"); }} //goes back to the previous screen when the go back button is pressed
        />
      </View>
      
      <Text style={{ position: "absolute", bottom: 40, right: 20, backgroundColor: "white", padding: 5, borderRadius: 5, borderColor: "grey", borderWidth: 1 }}>
        Room number: {user.room_number}
      </Text>


      </View>


  );
}

function GetMarkers(data: string | null, setMarkers: React.Dispatch<React.SetStateAction<{ id: string; type: string; latitude: number; longitude: number }[]>>) {
  if (data == null) return;
  if (data.startsWith("place_marker|")) {
    const parts = data.split("|");
    const new_marker = { id: parts[1], type: parts[2], latitude: parseFloat(parts[3]), longitude: parseFloat(parts[4]) };
    setMarkers(prev => {
      if (prev.some(m => m.id === new_marker.id)) return prev;
      return [...prev, new_marker];
    });
  } 
  else if (data.startsWith("remove_marker|")) {
    const markerId = data.split("|")[1];
    setMarkers(prev => prev.filter(marker => marker.id !== markerId));
  }
  console.log('passed')
}

const markerImages: { [key: string]: any } = {
  infantry: require("../assets/images/symbols/infantry.png"),
  tank: require("../assets/images/symbols/tank.png"),
  mechine_gunner: require("../assets/images/symbols/mechine_gunner.png"),
  target: require("../assets/images/symbols/target.png"),
  armor: require("../assets/images/symbols/armored_vehicle.png"),
  artillery: require("../assets/images/symbols/artillery.png"),
  attack_aircraft: require("../assets/images/symbols/attack_aircraft.png"),
  drone: require("../assets/images/symbols/drone.png"),
  helicopter: require("../assets/images/symbols/helicopter.png"),
  mortar: require("../assets/images/symbols/mortar.png"),
  outpost: require("../assets/images/symbols/outpost.png"),
  ship: require("../assets/images/symbols/ship.png"),
  sniper: require("../assets/images/symbols/sniper.png"),

  friendly_infantry: require("../assets/images/symbols/friendly_infantry.png"),
  friendly_tank: require("../assets/images/symbols/friendly_tank.png"),
  friendly_mechine_gunner: require("../assets/images/symbols/friendly_mechine_gunner.png"),
  friendly_armor: require("../assets/images/symbols/friendly_armored_vehicle.png"),
  friendly_artillery: require("../assets/images/symbols/friendly_artillery.png"),
  friendly_attack_aircraft: require("../assets/images/symbols/friendly_attack_aircraft.png"),
  friendly_drone: require("../assets/images/symbols/friendly_drone.png"),
  friendly_helicopter: require("../assets/images/symbols/friendly_helicopter.png"),
  friendly_mortar: require("../assets/images/symbols/friendly_mortar.png"),
  friendly_outpost: require("../assets/images/symbols/friendly_outpost.png"),
  friendly_ship: require("../assets/images/symbols/friendly_ship.png"),
  friendly_sniper: require("../assets/images/symbols/friendly_sniper.png"),
};

const styles = StyleSheet.create({
  map: { flex: 1 },
});