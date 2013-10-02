<?php
error_reporting(E_ALL);
class PDF2IMG {
  /**
   * @var string
   */
  var $base_url;

  /** 
   * @var string
   */
  var $application_id;

  /**
   * @var string
   */
  var $application_key;

  /**
   * @var string
   */
  var $output_format = 'tiff';

  /**
   * @var string
   */
  var $print_preview = TRUE;

  /**  
   * @param string     $version Version Number 
   */
  public function __construct($version = 0) {
    $this->base_url = "https://pdfprocess.datalogics-cloud.com/api/".$version."/actions/image";
  }  

  /** Set Application ID
   * @param string     $application_id
   */
  public function application_id($application_id) {
    $this->application_id = $application_id;
  }

  /** Set Application Key
   * @param string     $application_key
   */
  public function application_key($application_key) {
    $this->application_key = $application_key; 
  }

  /** Set output file format
   * @param string     $output_format  (jpg, tiff)
   */
  public function output_format($output_format = "jpg") {
    $this->output_format = $output_format;
  } 
 
  /** Set print preview
   * @param bool     $print_preview (true, false)
   */
  public function print_preview($print_preview = TRUE) {
   $this->print_preview = $print_preview;
  }
  

  /** Call server to convert file
   * @param string     $source_file_name Input file name
   * @param string     $destination_file_name Output file name
   */
  public function convert($source_file_name, $destination_file_name) {
    $ch = curl_init($this->base_url);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $this->prepare_request($source_file_name));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);  
    curl_setopt($ch, CURLOPT_VERBOSE, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: multipart/form-data'));
    $response = curl_exec($ch);
    curl_close($ch);
    $this->handle_response($response, $destination_file_name);
  }
  /** Handle server response
   * @param JSONObject     $response Server Response 
   * @param string         $destination_file_name output file name
   */
  public function handle_response($response, $destination_file_name) {
    $json_decoded = json_decode($response);
    $output = base64_decode($json_decoded->output);
    $file = fopen($destination_file_name, "wb");
    fwrite($file, $output);
    fclose($file);
  }

  private function prepare_request($file_name) {
    $fields = array(
      'application' => $this->prepare_application_json(), 
      'inputName' => basename($file_name),
      'options' => $this->prepare_options_json(),
      'input' => "@$file_name"
     );
    return $fields;
  }

  private function prepare_options_json() {
    $options = array();
    $options['outputForm'] = $this->output_format;
    if ($this->print_preview) {
     $options['printPreview'] = TRUE;
    }
    return json_encode($options);
  }
  
  private function prepare_application_json() {
    $application = array('id' => $this->application_id,
                         'key' => $this->application_key);
    return json_encode($application);
  }
}

// Driver code
$source_file_name = "./test.pdf";
$destination_file_name = "converted.jpg";
$pdf2img = new PDF2IMG();
$pdf2img->application_id = '84445ec0'; 
$pdf2img->application_key = '2d3eac77bb3b9bea69a91e625b9241d2';
$pdf2img->output_format = 'jpg';
$pdf2img->print_preview = FALSE;
$pdf2img->convert($source_file_name, $destination_file_name);

?>
