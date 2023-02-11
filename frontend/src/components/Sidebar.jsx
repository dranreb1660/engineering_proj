import React from "react";
import {
  Avatar,
  Divider,
  Flex,
  Heading,
  IconButton,
  Text,
  useMediaQuery,
} from "@chakra-ui/react";
import { useState, useEffect } from "react";
import { FiHome, FiMenu, FiInfo } from "react-icons/fi";
import { GiSoccerKick } from "react-icons/gi";
import { SideItem } from "./";
import { Link } from "react-router-dom";

const Sidebar = () => {
  const [isNotSmallScreen] = useMediaQuery("(min-width: 600px)");
  // const [isPhoneScreen] = useMediaQuery("(min-width: 400x)");
  const [navsize, setNavsize] = useState("large");
  const [selectedMenu, setSelectedMenu] = useState("/");
  // useEffect(() => {
  //   if (!isNotSmallScreen) {
  //     console.log("setting to small");
  //     setNavsize("small");
  //   }
  // }, [isNotSmallScreen]);

  console.log(isNotSmallScreen, navsize);
  return (
    <Flex
      position={"absolute"}
      top="15vh"
      left={"2%"}
      h="70vh"
      mt={"2.5vh"}
      boxShadow="outline"
      borderRadius={navsize === "small" ? "30px" : "50px"}
      w={navsize === "small" || !isNotSmallScreen ? "50px" : "200px"}
      flexDir="column"
      justifyContent={"space-between"}
    >
      <Flex p={"5%"} direction={"column"} alignItems="flex-start" as={"nav"}>
        <IconButton
          background={"none"}
          mt={5}
          icon={<FiMenu />}
          onClick={() => {
            navsize === "small" ? setNavsize("large") : setNavsize("small");
          }}
          alignSelf={navsize === "small" ? "center" : "flex-start"}
        />

        <SideItem
          navsize={navsize}
          icon={FiHome}
          item={"Homepage"}
          link="/"
          selectedMenu={selectedMenu}
          setSelectedMenu={setSelectedMenu}
        />

        <SideItem
          navsize={navsize}
          icon={GiSoccerKick}
          item={"Predict"}
          link="/auto_predict"
        />

        <SideItem
          navsize={navsize}
          icon={FiInfo}
          item={"About"}
          link="/about"
        />
      </Flex>
      <Flex
        p={"5%"}
        flexDir={"column"}
        w="100%"
        alignItems={
          navsize === "small" || !isNotSmallScreen ? "center" : "flex-start"
        }
      >
        <Divider />
        <Flex m={4} align="center" position={"relative"} bottom={0}>
          <Avatar size="sm" />
          <Flex
            direction={"column"}
            m={4}
            display={navsize === "small" || !isNotSmallScreen ? "none" : "flex"}
          >
            <Heading as="h3" size={"sm"}>
              Bernard Opoku
            </Heading>
            <Text color={"gray"}> MLE</Text>
          </Flex>
        </Flex>
      </Flex>
    </Flex>
  );
};

export default Sidebar;
