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

    // clear the staging coords so the preview pin disappears
    markerContext.setMark_latitude(null);
    markerContext.setMark_longitude(null);

    navigation.navigate("Home");
  }

  const buttons = [
  //ENEMY
  // Row 1
  { label: "Infantry", image: require("../assets/images/symbols/infantry.png"), left: 10, bottom: 700, onPress: () => SendChosenMarkToServer("Infantry") },
  { label: "Mechine_Gunner", image: require("../assets/images/symbols/mechine_gunner.png"), left: 100, bottom: 700, onPress: () => SendChosenMarkToServer("Mechine_Gunner") },
  { label: "Armor", image: require("../assets/images/symbols/armored_vehicle.png"), left: 200, bottom: 700, onPress: () => SendChosenMarkToServer("Armor") },
  { label: "Attack_Aircraft", image: require("../assets/images/symbols/attack_aircraft.png"), left: 300, bottom: 700, onPress: () => SendChosenMarkToServer("Attack_Aircraft") },

  // Row 2
  { label: "Tank", image: require("../assets/images/symbols/tank.png"), left: 10, bottom: 600, onPress: () => SendChosenMarkToServer("Tank") },
  { label: "Sniper", image: require("../assets/images/symbols/sniper.png"), left: 100, bottom: 600, onPress: () => SendChosenMarkToServer("Sniper") },
  { label: "Artillery", image: require("../assets/images/symbols/artillery.png"), left: 200, bottom: 600, onPress: () => SendChosenMarkToServer("Artillery") },
  { label: "Drone", image: require("../assets/images/symbols/drone.png"), left: 300, bottom: 600, onPress: () => SendChosenMarkToServer("Drone") },

  // Row 3
  { label: "Helicopter", image: require("../assets/images/symbols/helicopter.png"), left: 10, bottom: 500, onPress: () => SendChosenMarkToServer("Helicopter") },
  { label: "Mortar", image: require("../assets/images/symbols/mortar.png"), left: 100, bottom: 500, onPress: () => SendChosenMarkToServer("Mortar") },
  { label: "Outpost", image: require("../assets/images/symbols/outpost.png"), left: 200, bottom: 500, onPress: () => SendChosenMarkToServer("Outpost") },
  { label: "Ship", image: require("../assets/images/symbols/ship.png"), left: 300, bottom: 500, onPress: () => SendChosenMarkToServer("Ship") },

  // Extra
  { label: "Target", image: require("../assets/images/symbols/target.png"), left: 10, bottom: 400, onPress: () => SendChosenMarkToServer("Target") },

  //FRIENDLY
  // Row 4
  { label: "Friendly_Infantry", image: require("../assets/images/symbols/friendly_infantry.png"), left: 10, bottom: 300, onPress: () => SendChosenMarkToServer("Friendly_Infantry") },
  { label: "Friendly_Mechine_Gunner", image: require("../assets/images/symbols/friendly_mechine_gunner.png"), left: 100, bottom: 300, onPress: () => SendChosenMarkToServer("Friendly_Mechine_Gunner") },
  { label: "Friendly_Armor", image: require("../assets/images/symbols/friendly_armored_vehicle.png"), left: 200, bottom: 300, onPress: () => SendChosenMarkToServer("Friendly_Armor") },
  { label: "Friendly_Attack_Aircraft", image: require("../assets/images/symbols/friendly_attack_aircraft.png"), left: 300, bottom: 300, onPress: () => SendChosenMarkToServer("Friendly_Attack_Aircraft") },

  // Row 5 
  { label: "Friendly_Tank", image: require("../assets/images/symbols/friendly_tank.png"), left: 10, bottom: 200, onPress: () => SendChosenMarkToServer("Friendly_Tank") },
  { label: "Friendly_Sniper", image: require("../assets/images/symbols/friendly_sniper.png"), left: 100, bottom: 200, onPress: () => SendChosenMarkToServer("Friendly_Sniper") },
  { label: "Friendly_Artillery", image: require("../assets/images/symbols/friendly_artillery.png"), left: 200, bottom: 200, onPress: () => SendChosenMarkToServer("Friendly_Artillery") },
  { label: "Friendly_Drone", image: require("../assets/images/symbols/friendly_drone.png"), left: 300, bottom: 200, onPress: () => SendChosenMarkToServer("Friendly_Drone") },

  // Row 6 
  { label: "Friendly_Helicopter", image: require("../assets/images/symbols/friendly_helicopter.png"), left: 10, bottom: 100, onPress: () => SendChosenMarkToServer("Friendly_Helicopter") },
  { label: "Friendly_Mortar", image: require("../assets/images/symbols/friendly_mortar.png"), left: 100, bottom: 100, onPress: () => SendChosenMarkToServer("Friendly_Mortar") },
  { label: "Friendly_Outpost", image: require("../assets/images/symbols/friendly_outpost.png"), left: 200, bottom: 100, onPress: () => SendChosenMarkToServer("Friendly_Outpost") },
  { label: "Friendly_Ship", image: require("../assets/images/symbols/friendly_ship.png"), left: 300, bottom: 100, onPress: () => SendChosenMarkToServer("Friendly_Ship") },

  
];
 //each button is absolutely positioned on a grid — left sets the column, bottom sets the row 
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
