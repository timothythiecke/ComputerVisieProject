use Cwd qw(cwd);
use File::Copy;

my $imageNum = 0;
my $max = 30;

recursive_dir("C:\\Users\\counterpoint\\Desktop\\ComputerVisieProject\\Images\\TestSet\\single_paintings");

sub recursive_dir {

    my $directory = shift; 
    opendir my $dh, $directory or die "$!\n"; 
    my @content = readdir $dh;
    # Removes . and .. pseudodirectories (they are the zero-th and first element)
    # Also removes the annoying 'System Volume Information folder', if it exists. It will always be the second element.
    @content = @content[2 + (scalar @content > 2 ? $content[2] eq 'System Volume Information' : 0) .. $#content]; 
    if(@content){
        foreach my $el (@content){
            my $fullpath = "$directory\\$el"; # append base path
        
            if(-d $fullpath){
                print  "[$el]\n";
                recursive_dir($fullpath)
            }
            
            if(-f $fullpath){         
                my $random = rand(1);
                if($random > 0.3 && $imageNum < $max) {
                    $imageNum++;
                    print  "- $el\n";  
                    copy($fullpath, "C:\\Users\\counterpoint\\Desktop\\ComputerVisieProject\\Images\\TestSet\\$imageNum.jpg");
                }   
            }          
        }
    }else{
        print $logfh "- No content\n";
    }
}
