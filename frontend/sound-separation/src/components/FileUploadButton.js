import React from "react";

function FileUploadButton() {
  return (
    <form action="/upload" method="post" encType="multipart/form-data">
      <label htmlFor="file">Select a file to upload </label>
      <input type="file" id="qa-id-upload-file" name="file" />
      <button type="submit">Upload</button>
    </form>
  );
}

export default FileUploadButton;
