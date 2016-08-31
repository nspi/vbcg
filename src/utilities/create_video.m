%CREATE_VIDEO   Creates a video for testing purposes
% CREATE_VIDEO(X) creates a 90s video (.avi) and the individual frames (.png) 
% on the hard disk. It shows a repeating pattern from black to white
% frames and X defines the frequency (in Hz) of this pattern. FPS defines
% the FPS of the synthetic video.
%
% The video imitates the skin color variations associated to the pulse.
% It was used used to determine if the computed HR is stable.
%
% Usage:
%    create_video(1,25) -> Creates video with 1 Hz pulse signal and 25 FPS

function create_video(X,FPS)

    % Initialize video
    file_name = ['synthetic_video_',num2str(X),'_',num2str(FPS),'.avi'];
    writerObj = VideoWriter(file_name);
    writerObj.FrameRate = FPS;
    open(writerObj);
    
    % Create folder for frames
    mkdir(['img_',num2str(X),'_',num2str(FPS)])
    
    % Print message
    disp(['Create video: ', file_name]) 

    % Set resolution
    x_dim = 480;
    y_dim = 640;

    % Duration of video in seconds
    dur = 90;
    
    % Inverse of FPS
    step_size = 1/FPS;

    % Time axis 
    t = 0:step_size:dur-step_size;

    % Main signal
    signal = (cos(2*pi*X*t));

    % Normalize to [0,1]
    signal = (signal-min(signal))/(max(signal)-min(signal));

    % Create empty video matrix
    video_mat = zeros(x_dim,y_dim,size(signal,2));

    % Fill video matrix
    for i=1:x_dim
        for j=1:y_dim
            video_mat(i,j,:) = signal;
        end
    end

    % Iterate throughout each frame and store it in video and as .png
    for i=1:size(signal,2)
        % Get frame
        I = video_mat(:,:,i);
        % Write to video
        writeVideo(writerObj,I);
        % Write to hard disk
        imwrite(I,['img_',num2str(X),'_',num2str(FPS),'/',num2str(i),'.jpg']);
        
        % Display status
        if mod(i,100)==0
            disp(['Processing:',num2str(i/size(signal,2)),'%']);
        end
    end

    % Close video
    close(writerObj);

end
