import { createNativeStackNavigator } from "@react-navigation/native-stack";
import React, { useState } from "react";
import Home from "../components/Home";
import Login from "../components/login";
import MarkerSelect from "../components/MarkerSelect";
import { MarkerContext,UserContext } from "../context/AppContext";
import useWebSocket from "../hook/useWebSocket";

const Stack = createNativeStackNavigator();

export default function RootLayout() {
  const [userId, setUserId] = useState<string | null>(null);
  const [room_number, setRoom_number] = useState<string | null>(null);
  const webSocket = useWebSocket("10.100.102.14", 3000);

    // staging coords for a marker before the user picks its type
  const [Mark_latitude, setMark_latitude] = useState<number | null>(null);
  const [Mark_longitude, setMark_longitude] = useState<number | null>(null);
  const [ChosenMark, setChosenMark] = useState<string | null>(null);

  return (
        // two separate contexts — one for the map marker state, one for the user/socket session
    <MarkerContext.Provider
      value={{ 
        Mark_latitude,
        setMark_latitude,
        Mark_longitude,
        setMark_longitude,
        ChosenMark,
        setChosenMark,
      }}
    >
      <UserContext.Provider value={{ webSocket, userId, setUserId, room_number, setRoom_number }}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen name="Login" component={Login} />
          <Stack.Screen name="Home" component={Home} />
          <Stack.Screen name="MarkerSelect" component={MarkerSelect} />
        </Stack.Navigator>
      </UserContext.Provider>
    </MarkerContext.Provider>
  );
}
