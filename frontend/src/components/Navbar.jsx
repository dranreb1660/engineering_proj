import {
  Box,
  Center,
  Flex,
  Heading,
  IconButton,
  Spacer,
  useColorMode,
} from "@chakra-ui/react";
import { FaSun, FaMoon } from "react-icons/fa";
import React from "react";

const Navbar = () => {
  const { colorMode, toggleColorMode } = useColorMode();
  const isDark = colorMode === "dark";
  return (
    <Center top={"20px"} position="sticky" zIndex={10}>
      <Flex
        width={"70%"}
        h={"32px"}
        rounded="2.5vh"
        bgGradient={
          isDark
            ? "linear(to-r, cyan.900,gray.800, blue.900, green.900)"
            : "linear(to-r, cyan.400, blue.500, green.600, green.800)"
        }
        boxShadow="outline"
      >
        <Heading
          size={"md"}
          ml="10px"
          mt={"5px"}
          bgGradient={"linear(to-r,pink.800, cyan.900, blue.500, purple.600)"}
          bgClip="text"
        >
          Bern.A.i
        </Heading>
        <Spacer />
        <IconButton
          icon={isDark ? <FaSun /> : <FaMoon />}
          onClick={toggleColorMode}
          isRound="true"
          size="sm"
        />
      </Flex>
    </Center>
  );
};

export default Navbar;
