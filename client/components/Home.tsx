import React from "react";
import { StyleSheet } from "react-native";
import MapView, { Marker } from "react-native-maps";

export default function MapScreen() {
  return (
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
  );
}

const styles = StyleSheet.create({
  map: {
    flex: 1,
  },
});
