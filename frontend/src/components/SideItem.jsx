import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { useState } from "react";
import {
  Flex,
  Link,
  Menu,
  MenuButton,
  Text,
  Icon,
  useMediaQuery,
} from "@chakra-ui/react";

const SideItem = ({
  navsize,
  item,
  icon,
  link,
  selectedMenu,
  setSelectedMenu,
}) => {
  // || !isNotSmallScreen
  const [isNotSmallScreen] = useMediaQuery("(min-width: 600px)");
  const active = selectedMenu === link;

  return (
    <Flex
      mt={30}
      direction="column"
      w={"100%"}
      alignItems={
        navsize === "small" || !isNotSmallScreen ? "center" : "flex-start"
      }
    >
      <Menu placement="right">
        <Link
          bgColor={active && "#AEC8CA"}
          p={3}
          borderRadius={8}
          _hover={{ textColor: "none", backgroundColor: "#AEC8CA" }}
          w={navsize === "large" && "100%"}
          as={RouterLink}
          to={link}
          onClick={() => {
            setSelectedMenu(link);
            console.log(selectedMenu);
          }}
        >
          <MenuButton w={"100%"}>
            <Flex>
              <Icon
                as={icon}
                fontSize="xl"
                color={active ? "82AAAD" : "gray.500"}
              />
              <Text
                ml={5}
                display={
                  navsize === "small" || !isNotSmallScreen ? "none" : "flex"
                }
              >
                {item}
              </Text>
            </Flex>
          </MenuButton>
        </Link>
      </Menu>
    </Flex>
  );
};

export default SideItem;
