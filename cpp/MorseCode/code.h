#ifndef MORSE_CODE_H
#define MORSE_CODE_H

#include <iostream>
#include <fstream>
#include <string>
#include <map>

const char *MORSE_FILE = "../data/Morse.txt";
const char *BRAILLE_FILE = "../data/Braille.txt";

void die(const std::string &msg) {
    std::cerr << msg << std::endl;
    exit(-1);
}

class Code {
public:
    Code() = default;

    explicit Code(const std::string &code_file, const char delimiter = ' ') : _delimiter(delimiter) {
        construct_code_map(code_file);
    }

    std::string encode(const std::string &ascii_string, bool exit_on_error = true) {
        std::string result;
        for (auto &ascii_char : ascii_string) {
            if (exit_on_error && _ascii2code.count(ascii_char) == 0)
                die(std::string("Invalid char '") + ascii_char + "'.");
            result += _ascii2code[ascii_char] + _delimiter;
        }
        return result.substr(0, result.length() - 1);
    }

    std::string decode(const std::string &code_string, bool exit_on_error = true) {
        std::string code_msg(code_string);
        if (code_msg[code_msg.length() - 1] != ' ') code_msg += ' ';
        std::string result, code;
        unsigned offset, last_offset = 0;
        while ((offset = code_msg.find(_delimiter, last_offset)) != -1) {
            code = code_msg.substr(last_offset, offset - last_offset);
            last_offset = offset + 1;
            if (exit_on_error && _code2ascii.count(code) == 0)
                die(std::string("Invalid code '") + code + "'.");
            result += _code2ascii[code];
        }
        return result;
    }

private:
    void construct_code_map(const std::string &code_file) {
        std::ifstream fin(code_file);
        char ascii_char;
        std::string code;
        if (!fin)
            die(std::string("Cannot open file: ") + code_file);
        while (!fin.eof()) {
            fin >> ascii_char >> code;
            if (ascii_char == '_') ascii_char = _delimiter;
            _ascii2code[ascii_char] = code;
            _code2ascii[code] = ascii_char;
        }
        fin.close();
    }

protected:
    std::map<char, std::string> _ascii2code;
    std::map<std::string, char> _code2ascii;
    char _delimiter{' '};
};

class MorseCode : public Code {
public:
    explicit MorseCode(char delimiter = ' ') : Code(MORSE_FILE, delimiter) {}
};

class BrailleCode : public Code {
public:
    explicit BrailleCode(char delimiter = ' ') : Code(BRAILLE_FILE, delimiter) {}
};


#endif //MORSE_CODE_H
