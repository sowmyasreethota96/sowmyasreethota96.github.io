import * as React from "react"
import {
  ChakraProvider,
  Box,
  Text,
  Link,
  VStack,
  Code,
  Grid,
  theme,
} from "@chakra-ui/react"
import { ColorModeSwitcher } from "./ColorModeSwitcher"
import { Logo } from "./Logo"
import { SeamCarver } from "./SeamCarver"

export const App = () => (
  <ChakraProvider theme={theme}>
    <Box textAlign="center" fontSize="xl">
      <Text color={"#660000"} fontSize="4xl" textAlign={'center'}>
        <b>CSCE 646 Project 2 - Seam Carver</b>
      </Text>
      <Text>
        Reuben Chidubem Tabansi
      </Text>
    </Box>
    <SeamCarver/>
  </ChakraProvider>
)
