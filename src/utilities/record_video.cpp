/** record_video.cpp
*
* a very simple c++ script for recording a video with a OpenCV-compatible camera
* .jpg files are written to folder img/ and time stamp is stored in log.txt
*  If .read() fails, an error message is stored in log.txt
*
* Script supports Linux only (because it uses shell commands) and required OpenCV2
*
* build with:
* 	g++ -I/usr/local/include/opencv -I/usr/local/include/opencv2 -L/usr/local/lib/ -g -o record_video record_video.cpp `pkg-config opencv --cflags --libs`
*
* start with:
*	./record_video
*
*/

#include <opencv2/opencv.hpp>
#include <iostream>
#include <sstream>
#include <sys/stat.h>
#include <unistd.h>
#include <string>

using namespace cv;

void perform_shell_command(std::string command)
{
    std::stringstream ss;
    ss << command;
    system(ss.str().c_str());
    ss.str("");
}

int main( int argc, const char** argv )
{
    // Parameter: FPS of camera
    int fps = 30;
    // Parameter: Recording duration in sec
    int sec = 60;

    // OpenCV video capture
    cv::VideoCapture capture(0);
    // Contains file name of frame
    char file[10];
    // Needed for string functions
    std::stringstream ss;
    // Increases when .read() fails
    int missed_frames = 0;

    if (!capture.isOpened())
    {
        std::cout << "No webcam detected at specified port!" << std::endl;
        exit(0);
    }
    else
    {
        // Will contain frame
        Mat frame;

        // Print status message and current time
        std::cout << "Recording video" << std::endl;
        perform_shell_command("date +%H:%M:%S.%N");

        // Loop that iterates until all frames are acquired
        for (int i=0; i<fps*sec; i++)
        {
            std::cout << "Current frame: " << i << std::endl;
            // Try to read frame
            bool success = capture.read(frame);
            if (success)
            {
                // Store frame and corresponding time stamp in .log
                sprintf(file,"img/i%d.jpg",i);
                imwrite(file,frame);
                perform_shell_command("date +%H:%M:%S.%N >> log.txt");
            }
            else
                // Store error in .log
                perform_shell_command("echo ""ERROR: No frame acquired"" >> log.txt");
        }
        // Print status message and current time
        std::cout << "Recording finished. Missed frames:  " <<  missed_frames << std::endl;
        perform_shell_command("date +%H:%M:%S.%N");

        // Release camera and exit program
        capture.release();
        exit(0);
    }
}

