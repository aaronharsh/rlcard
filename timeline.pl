#!/usr/bin/env perl

use strict;
use warnings;


my $timestep;
my @cards_probses;

my %cards_probs_by_timestep;

sub note_results {
    return unless $timestep;

    $cards_probs_by_timestep{$timestep} = [ @cards_probses ];
}

sub array_keys {
    return map { $_[$_] } grep { $_ % 2 == 0 } 0..$#_;
}

sub array_values {
    return map { $_[$_] } grep { $_ % 2 == 1 } 0..$#_;
}


while (<>) {
    if (/^\s*timestep\s*\|\s*(\d+)/) {
        note_results();
        $timestep = $1;
        @cards_probses = ();
    }
    elsif (/^Evaluation of.*probs = \[([^]]*)\]$/) {
        my $cps = $1;
        push @cards_probses, [ $cps =~ /\('([^']*)', ([\d.]+)\)/g ];
    }
}

note_results();


if (%cards_probs_by_timestep) {
    my $has_printed_header;

    foreach my $timestep (sort { $a <=> $b } keys %cards_probs_by_timestep) {
        my $cards_probs = $cards_probs_by_timestep{$timestep};

        if (!$has_printed_header++) {
            print 'timestep';
            foreach my $cards_probs (@$cards_probs) {
                my @cards = array_keys(@$cards_probs);
                foreach my $card (@cards) {
                    print '|', '(' . join(',', @cards) . ')->' . $card;
                }
            }
            print "\n";
        }

        print join('|', $timestep, map { array_values(@$_) } @$cards_probs), "\n";
    }
}


__END__

----------------------------------------
  timestep     |  2
  reward       |  -0.77
----------------------------------------
Evaluation of ['5-H', 'A-S']: choose 5-H, probs = [('A-S', 0.3863632685585347), ('5-H', 0.6136367314414654)]
Evaluation of ['A-S', '5-H']: choose 5-H, probs = [('A-S', 0.3863632685585347), ('5-H', 0.6136367314414654)]
Evaluation of ['A-S', '5-D']: choose A-S, probs = [('A-S', 0.5118043423181955), ('5-D', 0.4881956576818045)]
Evaluation of ['J-S', '5-D']: choose 5-D, probs = [('5-D', 0.5140543138498379), ('J-S', 0.4859456861501621)]
Evaluation of ['J-S', '10-D']: choose J-S, probs = [('10-D', 0.48414812954360054), ('J-S', 0.5158518704563995)]
