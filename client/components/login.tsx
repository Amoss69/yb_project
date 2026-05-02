import { useNavigation, useFocusEffect } from "@react-navigation/native";
import React, { useContext, useEffect, useState } from "react";
import { BackHandler, Button, Text, TextInput, View } from "react-native";
import { UserContext } from "../context/AppContext";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [room, setRoom] = useState("");
  const [message, setMessage] = useState("");
  const user = useContext(UserContext);
  const navigation = useNavigation();

  if (!user) return null;
  const { webSocket, setUserId, room_number, setRoom_number } = user;

  useEffect(() => {
    // disable android back button so users can't go back to a previous session
    const backHandler = BackHandler.addEventListener("hardwareBackPress", () => true); //remove the ability to go back to the previous screen (using back button on android))
    return () => backHandler.remove();
  }, []);

  useEffect(() => {
    webSocket.setOnMessage((msg) => {
      if (msg.includes("login|success")) {
        setUserId(msg.split("|")[2]);

        navigation.navigate("Home");
      } else if (msg.includes("login|error|room_error")) {
        setMessage("Invalid room number");
      }
      else if (msg.includes("login|error")){
        setMessage("Invalid username or password");
      }
    });

    return () => webSocket.setOnMessage(null);
  }, );

  return (
    <View style={{ flex: 1, alignItems: "center", top: 20, padding: 20 }}>
      <Text>Username:</Text>
      <TextInput
        style={{ height: 40, width: 200, borderColor: "gray", borderWidth: 1, padding: 10, margin: 10 }}
        placeholder="Enter Username here"
        value={username}
        onChangeText={(text) => setUsername(text)}
      />

      <Text>Password:</Text>
      <TextInput
        style={{ height: 40, width: 200, borderColor: "gray", borderWidth: 1, padding: 10, margin: 10 }}
        placeholder="Enter Password here"
        value={password}
        onChangeText={(text) => setPassword(text)}
        secureTextEntry={true}
      />

      <Text>Room:</Text>
      <TextInput
        style={{ height: 40, width: 200, borderColor: "gray", borderWidth: 1, padding: 10, margin: 10 }}
        placeholder="Room number"
        value={room}
        onChangeText={(text) => {setRoom(text); setRoom_number(text)}} // keep both local and context in sync
      />

      <Button
        title="Login"
        onPress={() => {
          if (!username || !password || !room) {
            setMessage("Please fill all fields");
            return;
          }
          webSocket.sendData("login|" + username + "|" + password + "|" + room);
        }}
      />

      <Text>{message}</Text>

      <View style={{ position: "absolute", bottom: 50, left: 20 }}>
        <Button
          title = "exit"

          onPress={() => BackHandler.exitApp()} //exits the app when the exit button is pressed
        />
      </View>
    </View>
  );
}