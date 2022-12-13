import { Box, Button, Grid, GridItem, Image, Text } from "@chakra-ui/react"
import { useRef, useState } from "react";
import { FaCompressAlt, FaFileImage } from "react-icons/fa";
import defaultLeftImgSrc from './images/face3.jpg'
import defaultRightImgSrc from './images/face3_tilt.jpg'

export const SeamStitch = () => {
  const leftInputRef = useRef<HTMLInputElement>(null)
  const imageRef = useRef<HTMLImageElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  const [leftImageUrl, setLeftImageUrl] = useState(defaultLeftImgSrc);
  const [rightImageUrl, setRightImageUrl] = useState(defaultRightImgSrc);
  const [originalDimensions, setOriginalDimensions] = useState('')


  const leftHandleClick = () => {
    if (leftInputRef.current){
      leftInputRef.current.click();
    }
  }

  const leftFileSelect = (files: FileList | null) => {
    if (!files || !files.length) {
      return;
    }
    const imageURL = URL.createObjectURL(files[0]);
    
    setLeftImageUrl(imageURL)
  }

  const SetLeftSize = () => {
    if (imageRef.current) {
      setOriginalDimensions(imageRef.current.width + ' x ' + imageRef.current.height);
    }
  }

  return(
    <Box padding={8}>
      <Box marginBottom={'4'}>
        <Grid templateColumns='repeat(2, 1fr)' gap={6}>
          <GridItem w='100%'>
            <Box>
              <Button
                onClick={leftHandleClick}
                marginRight='5'
              >
                <FaFileImage />
                <Text marginLeft={'2'}><b>Upload Image</b></Text>
              </Button>
              {/* <Button
                onClick={resize}
              >
                <FaCompressAlt/>
                <Text marginLeft={'2'}><b>Resize</b></Text>
              </Button> */}
              
              <input
                style={{display:'none'}}
                type={'file'}
                accept={'image/png,image/jpeg'}
                ref={leftInputRef}
                onChange={(e) => {
                  const {files} = (e.target as HTMLInputElement);
                  leftFileSelect(files)
                }}
              />

              <Box>
                <Text fontSize={'3xl'}><b>Original Left Image:</b></Text>
                <Image marginBottom={'4'} ref={imageRef} src={leftImageUrl} onLoad={SetLeftSize}/>
                {/* <Text><b>Original Image Dimensions (W x H):</b> {originalDimensions}</Text> */}
              </Box>
            </Box>
          </GridItem>

          <GridItem w='100%'>
            <Box>
              <Button
                onClick={leftHandleClick}
                marginRight='5'
              >
                <FaFileImage />
                <Text marginLeft={'2'}><b>Upload Image</b></Text>
              </Button>
              {/* <Button
                onClick={resize}
              >
                <FaCompressAlt/>
                <Text marginLeft={'2'}><b>Resize</b></Text>
              </Button> */}
              
              <input
                style={{display:'none'}}
                type={'file'}
                accept={'image/png,image/jpeg'}
                ref={leftInputRef}
                onChange={(e) => {
                  const {files} = (e.target as HTMLInputElement);
                  leftFileSelect(files)
                }}
              />

              <Box>
                <Text fontSize={'3xl'}><b>Original Left Image:</b></Text>
                <Image marginBottom={'4'} ref={imageRef} src={leftImageUrl} onLoad={SetLeftSize}/>
                <Text><b>Original Image Dimensions (W x H):</b> {originalDimensions}</Text>
              </Box>
            </Box>
          </GridItem>
        </Grid>
      </Box>
    </Box>
  )
}