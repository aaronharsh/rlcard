#!/usr/bin/env perl

use strict;
use warnings;

use File::Basename qw(basename);


my $group_size = 10000;

my %files;
my %groups;

my %counts_by_file_group;
my %sum_loss_by_file_group;


foreach my $file (@ARGV) {
    my $base = basename($file);
    $base =~ s/^output-//;
    $base =~ s/,/x/g;

    $files{$base} = 1;

    open my $fh, '<', $file or die "Can't read $file: $!";
    while (<$fh>) {
        while (/Agent nfsp0_dqn, step (\d+), rl-loss: ([.\d]*\d)/g) {
            my $step = $1;
            my $loss = $2;

            my $group = int($step / $group_size);

            $groups{$group} = 1;
            $counts_by_file_group{$base}{$group}++;
            $sum_loss_by_file_group{$base}{$group} += $loss;
        }
    }
}

my @files = sort keys %files;

print join('|', 'group', @files), "\n";
foreach my $group (sort { $a <=> $b } keys %groups) {
    print $group;
    foreach my $file (@files) {
        my $count = $counts_by_file_group{$file}{$group};
        my $sum_loss = $sum_loss_by_file_group{$file}{$group};

        print '|';
        if ($count) {
            print $sum_loss / $count;
        }
    }
    print "\n";
}

__END__
----------------------------------------
  timestamp    |  2020-05-04 05:56:12
  timestep     |  2
  reward       |  -0.1662
----------------------------------------
Evaluation of ['A-S', '5-C', '5-H', '5-D']: choose A-S, probs = [('A-S', 0.30766039271671675), ('5-C', 0.23585892684143314), ('5-H', 0.24083382427009203), ('5-D', 0.21564685617175805)]
Evaluation of ['A-C', 'A-H', 'A-D', 'J-D']: choose A-D, probs = [('A-C', 0.1417882707195071), ('A-H', 0.21444494237249528), ('A-D', 0.3497132287423578), ('J-D', 0.2940535581656399)]
Evaluation of ['2-C', '3-H', '6-D', '7-D']: choose 2-C, probs = [('2-C', 0.26411833987298045), ('3-H', 0.24010953906571764), ('6-D', 0.25125885738838794), ('7-D', 0.24451326367291398)]
INFO - Agent nfsp0_dqn, step 1000, rl-loss: 0.6703484654426575
