import { useNavigation } from "@react-navigation/native";
import React, { useContext } from "react";
import { Image, TouchableOpacity, View } from "react-native";
import { MarkerContext, UserContext } from "../context/AppContext";

type ButtonProps = {
  label: string;
  image: any;
  left: number;
  bottom: number;
  onPress: () => void;
};

function Button({ label, image, left, bottom, onPress }: ButtonProps) {
  return (
    <TouchableOpacity
      onPress={onPress}
      style={{
        width: 60,
        height: 60,
        position: "absolute",
        left,
        bottom,
        alignItems: "center",
      }}
    >
      <Image source={image} style={{ width: "100%", height: "100%" }} />
    </TouchableOpacity>
  );
}

export default function MarkerSelect() {
  const navigation = useNavigation();
  const user = useContext(UserContext);
  const markerContext = useContext(MarkerContext);

  if (!user || !markerContext) return null;

  const { webSocket, userId } = user;

  function SendChosenMarkToServer(label: string) {
    const lat = markerContext.Mark_latitude;
    const lng = markerContext.Mark_longitude;

    if (lat == null || lng == null) {
      console.warn("No coordinates selected");
      return;
    }

    const payload = `marker|place|${label}|${lat}|${lng}`;
    webSocket.sendData(payload);

    markerContext.setMark_latitude(null);
    markerContext.setMark_longitude(null);

    navigation.navigate("Home");
  }

  const buttons = [
    {
      label: "Infantry",
      image: require("../assets/images/symbols/infantry.png"),
      left: 10,
      bottom: 700,
      onPress: () => SendChosenMarkToServer("Infantry"),
    },
    {
      label: "Mechine_Gunner",
      image: require("../assets/images/symbols/mechine_gunner.png"),
      left: 100,
      bottom: 700,
      onPress: () => SendChosenMarkToServer("Mechine_Gunner"),
    },
    {
      label: "Tank",
      image: require("../assets/images/symbols/tank.png"),
      left: 10,
      bottom: 600,
      onPress: () => SendChosenMarkToServer("Tank"),
    },
  ];

  return (
    <View style={{ flex: 1 }}>
      {buttons.map((button, index) => (
        <Button
          key={index}
          label={button.label}
          image={button.image}
          left={button.left}
          bottom={button.bottom}
          onPress={button.onPress}
        />
      ))}
    </View>
  );
}
