#!/usr/bin/perl
use strict;
use warnings;
use LWP::UserAgent;

if (@ARGV==0)
{
    print "batch_retrival UniProt_accession.list > UniProt_accession.fasta\n";
    exit(0);
}
my $list = $ARGV[0]; # File containg list of UniProt identifiers.

my $base = 'https://www.uniprot.org';
my $tool = 'uploadlists';

my $contact = 'zcx@umich.edu'; # Please set a contact email address here to help us debug in case of problems (see https://www.uniprot.org/help/privacy).
my $agent = LWP::UserAgent->new(agent => "libwww-perl $contact");
push @{$agent->requests_redirectable}, 'POST';

my $response = $agent->post("$base/$tool/",
                            [ 'file' => [$list],
                              #'format' => 'txt',
                              'format' => 'fasta',
                              'from' => 'ACC+ID',
                              'to' => 'ACC',
                              # If you want tab-separated output instead of full entries, specify 'tab' instead of 'txt' above
                              # and include the following optional line to include your preferred set of columns
                              # instead of the default from-to output:
                              #'columns' => 'id,entry name,reviewed,protein names,genes,organism,length,database(RefSeq),go(molecular function)',

                            ],
                            'Content_Type' => 'form-data');

while (my $wait = $response->header('Retry-After')) {
  print STDERR "Waiting ($wait)...\n";
  sleep $wait;
  $response = $agent->get($response->base);
}

$response->is_success ?
  print $response->content :
  die 'Failed, got ' . $response->status_line .
    ' for ' . $response->request->uri . "\n";
