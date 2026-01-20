import useWebSocket from "@/hook/useWebSocket";
import { useNavigation } from "@react-navigation/native";
import React, { useEffect, useState } from "react";
import { Button, Text, TextInput, View } from "react-native";

export default function Login({
  webSocket,
}: {
  webSocket: ReturnType<typeof useWebSocket>;
}) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigation = useNavigation();

  useEffect(() => {
    if (webSocket.lastMessage == "login|success") {
      navigation.navigate("Home");
    } else if (webSocket.lastMessage == "login|error|wrong_password") {
      setMessage("wrong password or username");
    } else if (webSocket.lastMessage == "login|error|no_user") {
      setMessage("wrong password or username");
    }
  }, [webSocket.lastMessage]);

  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        padding: 20,
      }}
    >
      <Text>Username:</Text>

      <TextInput
        style={{
          height: 40,
          width: 200,
          borderColor: "gray",
          borderWidth: 1,
          padding: 10,
          margin: 10,
        }}
        placeholder="Enter Username here"
        value={username}
        onChangeText={(text) => setUsername(text)}
      />

      <Text>Password:</Text>

      <TextInput
        style={{
          height: 40,
          width: 200,
          borderColor: "gray",
          borderWidth: 1,
          padding: 10,
          margin: 10,
        }}
        placeholder="Enter Password here"
        value={password}
        onChangeText={(text) => setPassword(text)}
      />

      <Button
        title="Login"
        onPress={() => webSocket.sendData("login|" + username + "|" + password)}
      />

      <Text>{message}</Text>
    </View>
  );
}
