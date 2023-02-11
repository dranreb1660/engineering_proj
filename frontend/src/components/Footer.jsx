import React from "react";
import { HStack, Icon, Center, VStack } from "@chakra-ui/react";
import { FaFacebook, FaLinkedin, FaGoogle, FaShopify } from "react-icons/fa";

const Social = () => {
  return (
    <Center
      position={"absolute"}
      bottom="10px"
      width={"100%"}
      justifySelf={"center"}
    >
      <HStack spacing={24}>
        <Icon as={FaFacebook} boxSize={"40px"} />
        <Icon as={FaLinkedin} boxSize={"40px"} />
        <Icon as={FaGoogle} boxSize={"40px"} />
        <Icon as={FaShopify} boxSize={"40px"} />
      </HStack>
    </Center>
  );
};

export default Social;
