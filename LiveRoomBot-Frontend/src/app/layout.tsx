import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";
import { Caveat, Jockey_One, Roboto } from "next/font/google";
import localFont from "next/font/local";

// Google fonts
const jockeyOne = Jockey_One({
  weight: "400",
  subsets: ["latin"],
  display: "swap",
  variable: "--font-jockey-one",
});

const roboto = Roboto({
  weight: ["400", "500", "700"],
  subsets: ["latin"],
  display: "swap",
  variable: "--font-roboto",
});

const caveat = Caveat({
  weight: "400",
  subsets: ["latin"],
  display: "swap",
  variable: "--font-caveat",
});

// Local fonts (from your public folder)
// Make sure your font files (e.g., Bruce.ttf) are located in the /public/fonts folder.
const bruce = localFont({
  src: "../../public/fonts/Bruce.ttf", // adjust the file extension if needed (e.g., .woff2)
  weight: "400",
  style: "normal",
  display: "swap",
  variable: "--font-Bruce-one",
});

const mangaregular = localFont({
  src: "../../public//fonts/mangaregular.ttf",
  weight: "400", // if you have multiple weights, create separate definitions or an array if supported
  style: "normal",
  display: "swap",
  variable: "--font-mangaregular",
});

const mangabold = localFont({
  src: "../../public//fonts/mangabold.ttf",
  weight: "700", // update as per your actual font weight
  style: "normal",
  display: "swap",
  variable: "--font-mangabold",
});

const pokemon = localFont({
  src: "../../public//fonts/Pokemon.ttf",
  weight: "400",
  style: "normal",
  display: "swap",
  variable: "--font-poky",
});

export const metadata: Metadata = {
  title: "Live Room",
  description: "Live Room, connect and create with your own buddy",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`
        ${jockeyOne.variable} 
        ${roboto.variable} 
        ${caveat.variable} 
        ${bruce.variable} 
        ${mangaregular.variable} 
        ${mangabold.variable} 
        ${pokemon.variable}
      `}
    >
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
