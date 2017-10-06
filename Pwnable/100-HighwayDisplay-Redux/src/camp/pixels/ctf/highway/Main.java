package camp.pixels.ctf.highway;

import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.inf.ArgumentParser;
import net.sourceforge.argparse4j.inf.ArgumentParserException;
import net.sourceforge.argparse4j.inf.Namespace;


public class Main {
	public static void main(String[] args) {
		
		ArgumentParser parser = ArgumentParsers.newArgumentParser("highway").defaultHelp(true);

        parser.addArgument("-l", "--listen").required(true)
                .dest("port")
                .help("Specify the port where the service should listen");

        int port = 0;
        try {
			Namespace ns = parser.parseKnownArgs(args, null);
	        port = Integer.parseInt(ns.get("port"));
        } catch (ArgumentParserException e) {
			parser.printHelp();
			System.exit(-1);
		}

		new DisplayController(new DisplayService(), port);
	}
}