```markdown
# Bitcoin Wallet Generator

This is a simple Python script that generates Bitcoin paper wallets and serves them through an HTTP server. It uses the `bit`, `Pillow`, and `qrcode` libraries for key generation, image manipulation, and QR code generation respectively.

## Requirements

- Python 3.5+
- `bit` library (`pip3 install bit`)
- `Pillow` library (`pip3 install Pillow`)
- `qrcode` library (`pip3 install qrcode`)

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/bitcoin-wallet-generator.git
   cd bitcoin-wallet-generator
   ```

2. Install the required libraries:

   ```bash
   pip3 install -r requirements.txt
   ```

3. Generate the SSL certificate and private key (for HTTPS):

   - If you already have an SSL certificate and private key, place them in the project directory with the following filenames:
     - Certificate: `fullchain.pem`
     - Private Key: `privkey.pem`

   - If you don't have an SSL certificate, you can generate a self-signed certificate using OpenSSL:

     ```bash
     openssl req -newkey rsa:2048 -nodes -keyout privkey.pem -x509 -days 365 -out fullchain.pem
     ```

     Follow the prompts to enter the necessary details. You may aslo choose to use Letsencrypt for SSL!

4. Run the server:

   ```bash
   python3 wallet_generator.py
   ```

5. Open your web browser and visit `https://localhost:8000` or your chosen domain to access the Bitcoin wallet generator.

## Usage

The web page will display the Bitcoin address, Segwit address, and private key (WIF format). It also provides a download link for the paper wallet image.

Click the "Generate New Address" button to create a new Bitcoin address and update the displayed details.

## Customization

- To use a different logo for the paper wallet, replace the `logo.png` file in the project directory with your own image.
- You can modify the HTML template in the `wallet_generator.py` file to customize the appearance of the wallet details page.
- To use custom fonts for the text on the paper wallet, copy your font files (`.ttf` or `.otf`) to the project directory and update the font paths in the `wallet_generator.py` file.

## Note


- The generated private keys are only displayed temporarily! Deletion time can be customized.
- Launch with screen and detach from session, change the port if you wish.
- If this helped you in some way please donate some BTC to: bc1qywm3pcgtwv2wx42ue9zelepdgukp4t94krh0va
