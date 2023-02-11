import React from "react";
import { useState, useEffect } from "react";
import {
  VStack,
  Center,
  Select,
  InputGroup,
  InputLeftAddon,
  useMediaQuery,
  Heading,
  Text,
  Box,
  Flex,
  Button,
  RadioGroup,
  Radio,
  Stack,
} from "@chakra-ui/react";

import { fetchInputs, fetchPrediction } from "../utils/fetchFromBackend";

const AutoPredictPage = () => {
  const [navsize, setNavsize] = useState("large");
  const [isNotSmallScreen] = useMediaQuery("(min-width: 600px)");

  const [player, setPlayer] = useState("");
  const [rounds, setRounds] = useState([]);
  const [round, setRound] = useState("");
  const [players, setPlayers] = useState([]);

  const [predictedScore, setPredictedScore] = useState(0);

  const submitHandler = () => {
    const pred = fetchPrediction({ player, round }).then((data) => {
      setPredictedScore(data.predicted);
    });
  };

  useEffect(() => {
    const { names, inputs } = fetchInputs().then((data) => {
      setPlayers(data.names);
      setRounds(data.rounds);
    });
  }, [predictedScore]);

  return (
    <VStack
      position="absolute"
      top={"15vh"}
      left={navsize === "small" || !isNotSmallScreen ? "100px" : "300px"}
    >
      <Center>
        <VStack>
          <Box mb={10}>
            <Heading>Predict Points</Heading>
            <Text>Predict a single player's projected points below</Text>
          </Box>

          <InputGroup>
            <InputLeftAddon
              pointerEvents={"none"}
              children="Player"
              p={4}
              mr={4}
              w={"10rem"}
              justifyContent="end"
              color={"blue.600"}
              fontWeight="bold"
            />
            <Select
              placeholder="Select Player to Predict"
              variant={"filled"}
              focusBorderColor="tomato"
              onChange={(e) => setPlayer(e.target.value)}
              value={player}
            >
              {players.map((playername, index) => (
                <option key={index} value={playername}>
                  {playername}
                </option>
              ))}
            </Select>
          </InputGroup>
          <InputGroup>
            <InputLeftAddon
              pointerEvents={"none"}
              children="Current GW?"
              p={4}
              mr={4}
              w={"10rem"}
              justifyContent="end"
              color={"blue.600"}
              fontWeight="bold"
            />
            <RadioGroup
              onChange={(e) => setRound(e.target.value)}
              value={round}
            >
              <Stack spacing={4} direction="row">
                <Radio value="yes">Yes</Radio>
                <Radio value="no">No</Radio>
              </Stack>
            </RadioGroup>
          </InputGroup>
          {round === "no" ? (
            <InputGroup>
              <InputLeftAddon
                pointerEvents={"none"}
                children="Gameweek"
                p={4}
                mr={4}
                w={"10rem"}
                justifyContent="end"
                color={"blue.600"}
                fontWeight="bold"
              />
              <Select
                placeholder="Select Gameweek to predict"
                variant={"filled"}
                focusBorderColor="tomato"
                onChange={(e) => setRound(e.target.value)}
                value={round}
              >
                {rounds.map((round, index) => (
                  <option key={index} value={round}>
                    {round}
                  </option>
                ))}
              </Select>
            </InputGroup>
          ) : (
            round === "yes" && setRound(rounds.slice(-1))
          )}

          <Button bg={"tomato"} color="white" size="lg" onClick={submitHandler}>
            {" "}
            Predict
          </Button>

          <Box pt={10}>
            <Flex>
              <Text as={"sub"}>Player is predicted to score: </Text>
              <Flex>
                <Heading px={5}>{predictedScore}</Heading>
                <Text mb={10} as="sub">
                  Points
                </Text>
              </Flex>
            </Flex>
          </Box>
        </VStack>
      </Center>
    </VStack>
  );
};

export default AutoPredictPage;
