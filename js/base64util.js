function base64Encode(str) {
  if (typeof window !== 'undefined' && typeof window.btoa === 'function') {
    // Browser environment
    return window.btoa(unescape(encodeURIComponent(str)));
  } else if (typeof Buffer !== 'undefined') {
    // Node.js environment
    return Buffer.from(str).toString('base64');
  } else {
    // Fallback or error handling
    return "Environment not supported";
  }
}

// Example usage:
// const originalString = "Hello, world! こんにちは、世界！";
// const encodedString = base64Encode(originalString);
// console.log("Encoded:", encodedString);

//Base64 decoding for browsers.
function base64Decode(str) {
  if (typeof window !== 'undefined' && typeof window.atob === 'function') {
      return decodeURIComponent(escape(window.atob(str)));
  } else if (typeof Buffer !== 'undefined'){
      return Buffer.from(str, 'base64').toString('utf-8');
  } else {
      return "Environment not supported";
  }

}

// const decodedString = base64Decode(encodedString);
// console.log("Decoded:", decodedString);

//Example of using a polyfill for older browsers that may not have atob and btoa built in.
//This is only needed for very old browsers.
if (typeof btoa === 'undefined') {
  (function() {
    var b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    window.btoa = function(bin) {
      for (var i = 0, j = 0, len = bin.length, base64 = ""; i < len; i += 3) {
        var byte1 = bin.charCodeAt(i),
          byte2 = bin.charCodeAt(i + 1),
          byte3 = bin.charCodeAt(i + 2),
          enc1 = byte1 >> 2,
          enc2 = ((byte1 & 3) << 4) | (byte2 >> 4),
          enc3 = isNaN(byte2) ? 64 : ((byte2 & 15) << 2) | (byte3 >> 6),
          enc4 = isNaN(byte2) || isNaN(byte3) ? 64 : byte3 & 63;
        base64 += b64.charAt(enc1) + b64.charAt(enc2) + b64.charAt(enc3) + b64.charAt(enc4);
      }
      return base64;
    };

    window.atob = function(base64) {
      for (var i = 0, j = 0, len = base64.length, bin = ""; i < len; i += 4) {
        var enc1 = b64.indexOf(base64.charAt(i)),
          enc2 = b64.indexOf(base64.charAt(i + 1)),
          enc3 = b64.indexOf(base64.charAt(i + 2)),
          enc4 = b64.indexOf(base64.charAt(i + 3)),
          byte1 = (enc1 << 2) | (enc2 >> 4),
          byte2 = ((enc2 & 15) << 4) | (enc3 >> 2),
          byte3 = ((enc3 & 3) << 6) | enc4;
        bin += String.fromCharCode(byte1);
        if (enc3 !== 64) bin += String.fromCharCode(byte2);
        if (enc4 !== 64) bin += String.fromCharCode(byte3);
      }
      return bin;
    };
  })();
}