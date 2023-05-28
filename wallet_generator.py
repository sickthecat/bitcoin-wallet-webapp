from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import ssl
from bit import Key
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import os
import uuid
import time
import threading

# Define the folder name to store temporary images
TEMP_FOLDER = "env_gen"

class BitcoinWalletHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/logo.png':
            # Serve the image file
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open('logo.png', 'rb') as image:
                self.wfile.write(image.read())
            return
        elif self.path.startswith('/sickw_'):
            # Serve the paper wallet image
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            filename = os.path.basename(self.path)
            with open(os.path.join(TEMP_FOLDER, filename), 'rb') as image:
                self.wfile.write(image.read())
            return
        else:
            # Create a new key
            k = Key()

            # Generate the private key in WIF format
            private_key = k.to_wif()

            # Get the Bitcoin address from the key
            bitcoin_address = k.address

            # Get the segwit Bitcoin address from the key
            segwit_address = k.segwit_address

            # Generate the paper wallet and get the filename
            filename = generate_paper_wallet(private_key, bitcoin_address, segwit_address)

            # Return wallet details as HTML with custom styling
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_template = """
            <html>
                <head>
                    <style>
                        body {{
                            background-color: black;
                            color: white;
                            font-size: small;
                            font-family: 'Courier New', Courier, monospace;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                        }}
                        .container {{
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            justify-content: center;
                            border: 1px solid grey;
                            padding: 10px;
                            text-align: center;
                            max-width: 500px;
                        }}
                        button {{
                            margin-top: 10px;
                        }}
                        .donation {{
                            position: absolute;
                            bottom: 10px;
                            left: 50%;
                            transform: translateX(-50%);
                            font-size: small;
                            text-align: center;
                        }}
                    </style>
                </head>
                <body>
                    <img src="logo.png" alt="sickthecat" style="position: absolute; top: 10px; left: 10px; width: 100px; height: 100px;">
                    <div class="container">
                        Bitcoin Address: {bitcoin_address}<br>
                        Segwit Address: {segwit_address}<br>
                        Private Key: {private_key}<br>
                        <br>
                        <a href="/{filename}" download="{filename}">Download Paper Wallet</a><br>
                        <br>
                        <form method="get" action="/">
                            <button type="submit">Generate New Address</button>
                        </form>
                    </div>
                    <div class="donation">
                        DOEN8 BTC TO: bc1qywm3pcgtwv2wx42ue9zelepdgukp4t94krh0va
                    </div>
                </body>
            </html>
            """.format(bitcoin_address=bitcoin_address, segwit_address=segwit_address, private_key=private_key, filename=filename)
            self.wfile.write(bytes(html_template, 'utf-8'))

def generate_paper_wallet(private_key, bitcoin_address, segwit_address):
    # Create a blank paper wallet image
    paper_wallet_image = Image.new("RGB", (1200, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(paper_wallet_image)

    # Load fonts for the text
    font_bold = ImageFont.truetype("arialbd.ttf", 32)
    font_normal = ImageFont.truetype("arial.ttf", 24)

    # Add Bitcoin logo
    bitcoin_logo = Image.open("logo.png")
    bitcoin_logo = bitcoin_logo.resize((100, 100), resample=Image.LANCZOS)
    paper_wallet_image.paste(bitcoin_logo, (10, 10))

    # Draw labels and text
    draw.text((130, 10), "Bitcoin Address", font=font_bold, fill=(0, 0, 0))
    draw.text((130, 70), bitcoin_address, font=font_normal, fill=(0, 0, 0))
    draw.text((130, 130), "Segwit Address", font=font_bold, fill=(0, 0, 0))
    draw.text((130, 190), segwit_address, font=font_normal, fill=(0, 0, 0))
    draw.text((130, 250), "Private Key (WIF)", font=font_bold, fill=(0, 0, 0))
    draw.text((130, 310), private_key, font=font_normal, fill=(0, 0, 0))

    # Generate a random filename for the paper wallet
    filename = "sickw_{}.jpg".format(uuid.uuid4())
    filepath = os.path.join(TEMP_FOLDER, filename)

    # Save the paper wallet image to a file
    paper_wallet_image.save(filepath, format="JPEG", quality=90)

    # Delete the file after 30 minutes
    def delete_file():
        try:
            os.remove(filepath)
        except OSError:
            pass

    # Schedule file deletion after 30 minutes
    threading.Timer(1800, delete_file).start()

    return filename

# Create the temporary folder if it doesn't exist
os.makedirs(TEMP_FOLDER, exist_ok=True)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == "__main__":
    httpd = ThreadedHTTPServer(('', 8000), BitcoinWalletHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   keyfile="privkey.pem",
                                   certfile='fullchain.pem', server_side=True)
    print("Server running on port 8000...")
    httpd.serve_forever()
