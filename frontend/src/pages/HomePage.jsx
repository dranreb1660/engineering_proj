import React from "react";

import {
  useMediaQuery,
  Stack,
  Circle,
  Flex,
  Box,
  Image,
  Text,
  Button,
  Center,
  useColorMode,
} from "@chakra-ui/react";

const HomePage = ({ isDark }) => {
  const [isNotSmallScreen] = useMediaQuery("(min-width: 600px)");
  //   const [isPhoneScreen] = useMediaQuery("(max-width: 400x)")
  return (
    <Center position="absolute" left={"200px"}>
      <Circle
        position={"absolute"}
        bg={isDark ? "blue.100" : "blue.800"}
        opacity={"0.2"}
        w="300px"
        h="300px"
        alignSelf={"flex-end"}
      />

      <Flex
        direction={isNotSmallScreen ? "row" : "column"}
        spacing="200px"
        p={isNotSmallScreen ? "32" : "0"}
      >
        <Box mt={isNotSmallScreen ? "0" : 16} alignSelf="flex-start">
          <Text fontSize={"3xl"} fontWeight="semibold">
            Welcome To
          </Text>
          <Text
            fontSize={"7xl"}
            fontWeight="bold"
            bgGradient={"linear(to-r, cyan.400, blue.500, purple.600)"}
            bgClip="text"
          >
            bern.A.i
          </Text>
          <Text color={isDark ? "gray.200" : "black"}>
            Your Number one stop for Fantasy Footbll prediction using
            Statistical Analysis, classical Machine Learning and modern Deep
            learning techniques
          </Text>
          <Button
            mt={8}
            colorScheme={"blue"}
            onClick={() => window.open("https://www.google.com")}
          >
            Lets Go...
          </Button>
        </Box>

        <Image
          mt={isNotSmallScreen ? "0" : 12}
          alignSelf="center"
          borderRadius={"full"}
          backgroundColor="transparent"
          boxShadow={"lg"}
          boxSize="300px"
          src="../assets/fpl-bg.jpg"
        />
      </Flex>
    </Center>
  );
};

export default HomePage;
