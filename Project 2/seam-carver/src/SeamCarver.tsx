import { useRef, useEffect, useState } from 'react';
import defaultImgSrc from './images/image_02.jpg';
import { Box, Button, Flex, Image, Input, NumberDecrementStepper, NumberIncrementStepper, NumberInput, NumberInputField, NumberInputStepper, Slider, SliderFilledTrack, SliderThumb, SliderTrack, Text} from "@chakra-ui/react";
import { FaCompressAlt, FaFileImage } from 'react-icons/fa';

export const SeamCarver = () => {
  const inputRef = useRef<HTMLInputElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);
  const [imageUrl, setImageUrl] = useState(defaultImgSrc);
  const [dimensions, setDimensions] = useState('')
  const handleClick = () => {
    if (inputRef.current){
      inputRef.current.click();
    }
  }

  const fileSelect = (files: FileList | null) => {
    if (!files || !files.length) {
      return;
    }
    const imageURL = URL.createObjectURL(files[0]);
    
    setImageUrl(imageURL);
    console.log(files);
  }

  const setSize = () => {
    console.log(imageRef)
    if (imageRef.current) {
      setDimensions(imageRef.current.width + ' x ' + imageRef.current.height);
    }
    
  }

  const [widthInput, setWidthInput] = useState(0)

  // useEffect(() => {
  //   if (imageRef.current) {
  //     setDimensions(imageRef.current.width + ' x ' + imageRef.current.height);
  //   }
  // }, [imageUrl]);

  // console.log(imageUrl);
  // console.log(imageRef);
  // console.log('d = ' + dimensions)

  return (
    <Box padding={8}>
      <Box marginBottom={'4'}>
        <Button
          onClick={handleClick}
          marginRight='5'
        >
          <FaFileImage />
          <Text marginLeft={'2'}><b>Upload Image</b></Text>
        </Button>
        <Button
          onClick={() => {console.log(imageUrl);}}
        >
          <FaCompressAlt/>
          <Text marginLeft={'2'}><b>Resize</b></Text>
        </Button>
        
        <input
          name='image_file'
          style={{display:'none'}}
          type={'file'}
          accept={'image/png,image/jpeg'}
          ref={inputRef}
          onChange={(e) => {
            const {files} = (e.target as HTMLInputElement);
            fileSelect(files)
          }}
        />
      </Box>
      
      <Box maxW={'600'} marginBottom='4'>
        <Flex>
          <Text marginRight={'3'} marginTop={'2'}>Width:</Text>
          <NumberInput maxW='100px' value={widthInput} onChange={(e) => {setWidthInput(Number(e))}}>
            <NumberInputField />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
          <Text marginTop={'2'} marginRight={'10'} marginLeft='2'>%</Text>
          <Slider
            flex='1'
            focusThumbOnChange={false}
            value={widthInput}
            onChange={(e) => {setWidthInput(e)}}
          >
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb fontSize='sm' boxSize='32px' children={widthInput} />
          </Slider>
        </Flex>
        
      </Box>
      <Box>
        <Text fontSize={'3xl'}><b>Original Image:</b></Text>
        <Image marginBottom={'4'} ref={imageRef} src={imageUrl} onLoad={setSize}/>
        <Text><b>Original Image Dimensions (W x H):</b> {dimensions}</Text>
      </Box>
    </Box>
  );
};