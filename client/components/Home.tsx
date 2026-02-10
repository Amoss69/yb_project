import { Button } from "@react-navigation/elements";
import React, { useState } from "react";
import { StyleSheet, View, Text, TouchableOpacity } from "react-native";
import MapView, { Marker } from "react-native-maps";

export default function MapScreen() {
  const [MessageMarker,setMessageMarker] = useState("");
  return (

    <View style={{
      width: '100%',
      height: '100%',
    }}> 
    
    <MapView
      style={styles.map}
      initialRegion={{
        latitude: 31.0461,
        longitude: 34.8516,
        latitudeDelta: 0.05,
        longitudeDelta: 0.05,
      }}
    >
      <Marker
        coordinate={{ latitude: 31.0461, longitude: 34.8516 }}
        title="Marker"
        description="This is a marker"
      />
    </MapView>


    <Button
    onPress={() => setMessageMarker("Choose point on mark")}
    style={{
      position: "absolute",
          bottom: 30,
          left: 20,
          backgroundColor: "#2196F3",
          paddingVertical: 12,
          paddingHorizontal: 20,
          borderRadius: 8,
    }}
    >
      <Text style={{color: "white", fontWeight: "bold", fontSize: 16}}>
        Create Marker
      </Text>
    </Button>
    

    <Text style={{
      position: "absolute", 
      bottom: 40,              
      left: 200,             
      fontSize: 16,
      color: "black",
      backgroundColor: "white",
      padding: 4,
      borderRadius: 4,
    }}>{MessageMarker}</Text>

    </View>


  );
}

const styles = StyleSheet.create({
  map: {
    flex: 1,
  },
});
